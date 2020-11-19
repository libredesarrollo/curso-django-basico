from django import template

register = template.Library()

@register.filter(name='discount')
def discount(element, coupon):
    return element.get_price_after_discount(coupon)

    