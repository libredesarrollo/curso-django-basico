from django.shortcuts import render, redirect,reverse, get_object_or_404
from django.core.paginator import Paginator
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.conf import settings
from django.utils import timezone
from django.http import HttpResponseNotFound, JsonResponse

from taggit.models import Tag

#import paypalrestsdk
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersCaptureRequest
from paypalhttp import HttpError
from decimal import Decimal

import logging

from listelement.models import Element, Category

from .models import Payment, Coupon
from .forms import MessageForm, CouponForm

from cart.cart import Cart

# Create your views here.

def index(request):
    search = request.GET.get('search') if request.GET.get('search') else ''
    category_id = request.GET.get('category_id')
    category_id = int(category_id) if category_id else ''

    tag_id = request.GET.get('tag_id')
    tag_id = int(tag_id) if tag_id else ''

    if search:
        elements = Element.objects.prefetch_related('elementimages_set').filter(title__contains=search)
    else:
        elements = Element.objects.prefetch_related('elementimages_set')

    if category_id:
        elements = elements.filter(category_id=category_id)

    if tag_id:
        tag = get_object_or_404(Tag,id=tag_id)
        elements = elements.filter(tags__in=[tag])
    
    elements = elements.filter(type = 1)
    paginator = Paginator(elements, 3)
    categories = Category.objects.all()
    tags = Tag.objects.all()    

    page_number = request.GET.get('page')
    elements_page = paginator.get_page(page_number)

    return render(request, 'store/index.html', {'elements' : elements_page,
                                        'categories':categories, 
                                        'tags' : tags,
                                        'search':search, 
                                        'category_id':category_id,
                                        'tag_id':tag_id
                                        })

def detail(request, url_clean, code=None):

    #print(code)


    #coupon= None
    #if code:
    #    coupon = get_valid_coupon(code)
    coupon = get_valid_coupon(code) if code else None

    msj_coupon =''
    if (code == 'None' or coupon is None) and code is not None:
        # el cupon es invalido
        msj_coupon ='El cupón es inválido'
        code = ''
        
    element = get_object_or_404(Element, url_clean=url_clean)

    if request.method == 'GET' and request.GET.get('quantity'):
        cart = Cart(request)
        cart.add(element, int(request.GET.get('quantity')))
        return redirect('store:detail',url_clean=element.url_clean)
        #for c in cart: print(c)


    messages = element.element_comments.filter(active=True)
    message_form = MessageForm(user=request.user)
    coupon_form = CouponForm(initial={'element_id':element.id,'code':code})
    message_new = None

    if request.method == 'POST':
        message_form = MessageForm(user=request.user,data=request.POST)
        if message_form.is_valid():
            message_new = message_form.save(commit=False)
            message_new.element = element
            if request.user.is_authenticated:
                message_new.name = request.user.first_name
                message_new.lastname = request.user.last_name
                message_new.email = request.user.email
                message_new.user = request.user
            message_new.save()
            message_form = MessageForm(user=request.user)

    cart = Cart(request)

    return render(request,'store/detail.html',{'element':element,
                                                'incart' : cart.getItem(element.id),
                                                'message_form': message_form,
                                                'message_new': message_new,
                                                'messages': messages,
                                                'coupon_form':coupon_form,
                                                'coupon': coupon,
                                                'msj_coupon':msj_coupon
    })

@require_POST
def coupon_apply(request):

    form = CouponForm(request.POST)
    coupon=None

    if form.is_valid():
        code = form.cleaned_data['code']
        elementId = form.cleaned_data['element_id']

    try:
        couponModel = get_valid_coupon(code)

        if couponModel:
            coupon = couponModel.code

    except Coupon.DoesNotExist:
        pass

    try:
        element = Element.objects.get(id=elementId)
    except Element.DoesNotExist:
        coupon=None

    return redirect('store:detail',url_clean=element.url_clean, code=coupon)


class DetailView(generic.DeleteView):
    model = Element
    template_name = 'store/detail.html'
    slug_field = 'url_clean'
    slug_url_kwarg = 'url_clean'

@login_required
def make_pay_paypal(request, pk, code=None):

    coupon = get_valid_coupon(code) if code else None

    #cupon invalido
    if coupon is None and code is not None:
        return HttpResponseNotFound()

    element = get_object_or_404(Element,pk = pk)

    if coupon:
        return_url = "http://127.0.0.1:8000/product/paypal/success/%s/%s"%(element.id,coupon.code)
        price = round(element.get_price_after_discount(coupon),2)
    else:
        return_url = "http://127.0.0.1:8000/product/paypal/success/%s"%element.id
        price = element.price

    client_id = settings.PAYPAL_CLIENT_ID
    client_secret = settings.PAYPAL_CLIENT_SECRET

    # Creating an environment
    environment = SandboxEnvironment(client_id=client_id, client_secret=client_secret)
    client = PayPalHttpClient(environment)

    requestPayPal = OrdersCreateRequest()

    requestPayPal.prefer('return=representation')

    requestPayPal.request_body (
        {
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "amount": {
                        "currency_code": "USD",
                        "value": str(price)
                    }
                }
            ],
            "application_context": {
                "return_url": return_url,
                "cancel_url": "http://127.0.0.1:8000/product/paypal/cancel"
            }
        }
    )

    try:
        # Call API with your client and get a response for your call
        response = client.execute(requestPayPal)

        if response.result.status == "CREATED":
            approval_url = str(response.result.links[1].href)
            print(approval_url)

            return render(request,'store/paypal/buy.html',{'element': element, 'approval_url':approval_url })

    except IOError as ioe:
        print (ioe)
        if isinstance(ioe, HttpError):
            # Something went wrong server-side
            print (ioe.status_code)


@login_required
def paypal_success(request,pk,code=None):

    coupon = get_valid_coupon(code) if code else None

    client_id = settings.PAYPAL_CLIENT_ID
    client_secret = settings.PAYPAL_CLIENT_SECRET

    # Creating an environment
    environment = SandboxEnvironment(client_id=client_id, client_secret=client_secret)
    client = PayPalHttpClient(environment)

    element = get_object_or_404(Element, pk = pk)

    ordenId = request.GET.get('token')
    payerId = request.GET.get('PayerID')

    requestPayPal = OrdersCaptureRequest(ordenId)

    try:
        # Call API with your client and get a response for your call
        response = client.execute(requestPayPal)

        paymentModel = Payment.create(payment_id=ordenId, 
            payer_id=payerId,
            price=element.price,
            element_id=element.id,
            user_id=request.user.id
        )

        if coupon:
            paymentModel.coupon = coupon
            paymentModel.discount = element.get_price_after_discount(coupon)
            paymentModel.price_discount = element.get_discount(coupon)
            coupon.active = 0
            coupon.save()

        paymentModel.save()

        # If call returns body in response, you can get the deserialized version from the result attribute of the response
        order = response.result.id
    except IOError as ioe:
        if isinstance(ioe, HttpError):
            # Something went wrong server-side
            print (ioe.status_code)
            print (ioe.headers)
            print (ioe)
        else:
            # Something went wrong client side
            print (ioe)

    return render(request,'store/paypal/success.html')



@login_required
def make_pay_paypal_old(request, pk, code=None):

    coupon = get_valid_coupon(code) if code else None

    #cupon invalido
    if coupon is None and code is not None:
        return HttpResponseNotFound()

    element = get_object_or_404(Element,pk = pk)

    if coupon:
        return_url = "http://127.0.0.1:8000/product/paypal/success/%s/%s"%(element.id,coupon.code)
        price = round(element.get_price_after_discount(coupon),2)
    else:
        return_url = "http://127.0.0.1:8000/product/paypal/success/%s"%element.id
        price = element.price

    paypalrestsdk.configure({
    "mode": settings.PAYPAL_CLIENT_MODO, 
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret":  settings.PAYPAL_CLIENT_SECRET})

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": return_url,
            "cancel_url": "http://127.0.0.1:8000/product/paypal/cancel"},
        "transactions": [{
            "amount": {
                "total": str(price),
                "currency": "USD"},
            "description": "This is the payment transaction description."}]})

    if payment.create():
        print("Payment created successfully")
    else:
        print(payment.error)

    for link in payment.links:
        if link.rel == "approval_url":
            # Convert to str to avoid Google App Engine Unicode issue
            # https://github.com/paypal/rest-api-sdk-python/pull/58
            approval_url = str(link.href)
            print("Redirect for approval: %s" % (approval_url))

    return render(request,'store/paypal/buy.html',{'element': element, 'approval_url':approval_url })

@login_required
def paypal_success_old(request,pk,code=None):

    coupon = get_valid_coupon(code) if code else None

    paypalrestsdk.configure({
    "mode": settings.PAYPAL_CLIENT_MODO, 
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret":  settings.PAYPAL_CLIENT_SECRET})


    element = get_object_or_404(Element, pk = pk)

    paymentId = request.GET.get('paymentId')
    payerId = request.GET.get('PayerID')

    payment = paypalrestsdk.Payment.find(paymentId)

    try:
        if payment.execute({"payer_id": payerId}):

            paymentModel = Payment.create(payment_id=paymentId, 
                payer_id=payerId,
                price=element.price,
                element_id=element.id,
                user_id=request.user.id
            )

            if coupon:
                paymentModel.coupon = coupon
                paymentModel.discount = element.get_price_after_discount(coupon)
                paymentModel.price_discount = element.get_discount(coupon)
                coupon.active = 0
                coupon.save()

            paymentModel.save()

            print("Payment execute successfully")

            return redirect(reverse('store:detail_pay',args=[paymentModel.id]))

        else:
            print(payment.error) # Error Hash
    except paypalrestsdk.exceptions.ResourceNotFound as e:
        print("UN error a ocurrido %s"%type(e).__name__)
    return render(request,'store/paypal/success.html')

@login_required
def detail_pay(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    return render(request,'store/payment/detail.html',{'payment':payment})

@login_required
def bought(request):
    return render(request,'store/payment/bought.html',{'payments':Payment.objects.select_related('element').filter(user = request.user)})

@login_required
def paypal_cancel(request):
    return render(request,'store/paypal/cancel.html')


# otras funciones
def get_valid_coupon(code):
    now = timezone.now()

    coupon = None
    try:
        couponModel = Coupon.objects.get(code__iexact=code,
            valid_from__lte=now, #less than or equal to
            valid_to__gte=now, #great than or equal to
            active=True
        )
        coupon = couponModel
    except Coupon.DoesNotExist:
        pass

    return coupon

# -----  carrito

def cart_detail(request): return render(request, 'cart/detail.html', {'cart' : Cart(request)})

def cart_remove(request, pk):
    cart = Cart(request)
    element = get_object_or_404(Element,pk=pk)

    cart.remove(element)
    return redirect('store:cart_detail')

def cart_size(request):
    cart = Cart(request)
    return JsonResponse({'size' : len(cart)})

def add_to_cart(request, pk):
    element = get_object_or_404(Element, pk=pk)

    cart = Cart(request)
    item = cart.add(element=element, quantity=int(request.GET.get('quantity')), override_quantity=True )



    return JsonResponse({'e_price': Decimal(item['price']) * item['quantity'],'price' : cart.get_total_price()})