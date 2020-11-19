from django.db import models
from django.contrib.auth.models import User

from django.core.validators import MinValueValidator, MaxValueValidator

from listelement.models import Element

# Create your models here.


class Coupon(models.Model):
    code = models.CharField(max_length=60, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    active = models.BooleanField()

    def __str__(self):
        return self.code

class Payment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    uptated_at = models.DateTimeField(auto_now=True)
    payment_id = models.CharField(max_length=200)
    payer_id = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10,decimal_places=2, default=6.10) # 12345678.10
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    element = models.ForeignKey(Element, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, null=True)
    discount = models.DecimalField(max_digits=10,decimal_places=2,  null=True) # 12345678.10
    price_discount = models.DecimalField(max_digits=10,decimal_places=2,  null=True) # 12345678.10

    @classmethod
    def create(cls, payment_id, payer_id, price, user_id, element_id):
        #super(Payment,self).__init__()

        payment = cls(
            payment_id=payment_id, 
            payer_id=payer_id,
            price=price,
            element_id=element_id,
            user_id=user_id
        )

        return payment

        """self.payment_id = payment_id
        self.payer_id = payer_id
        self.price = price
        self.user = user_id
        self.element = element_id"""

    def __str__(self):
        return self.price

class Message(models.Model):
    element = models.ForeignKey(Element, on_delete=models.CASCADE, related_name='element_comments')
    name = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return "Comentario de {self.name} en {self.element}"
