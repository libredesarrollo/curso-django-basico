from decimal import Decimal

from taggit.managers import TaggableManager

from django.db import models
from stdimage import StdImageField, JPEGField

from django.dispatch import receiver
from django.conf import settings

from django.urls import reverse

from django.utils.text import slugify

import os

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=255)
    url_clean = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class Type(models.Model):
    title = models.CharField(max_length=255)
    url_clean = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class Element(models.Model):
    tags = TaggableManager()
    title = models.CharField(max_length=255)
    url_clean = models.SlugField(max_length=255,blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10,decimal_places=2, default=6.10) # 12345678.10
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.url_clean = slugify(self.title)
        super(Element, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('store:detail', args=[self.url_clean])

    def get_discount(self, coupon):
        return (coupon.discount / Decimal(100)) * self.price # 10 /100 = 0.1 * 10$ = 1$

    def get_price_after_discount(self, coupon):
        return self.price - self.get_discount(coupon)

    def __str__(self):
        return self.title

class ElementImages(models.Model):
    element = models.ForeignKey(Element,on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    cover = JPEGField(upload_to='images/',variations={'custom': {'width': 550, 'height': 750, "crop": True}})
    base_cover_name = models.CharField(max_length=100, default='')
    base_cover_ext = models.CharField(max_length=5, default='')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):

        (root, ext) = os.path.splitext(self.cover.path)

        print(settings.MEDIA_ROOT)
        print(root)

        if(self.base_cover_name == ""):
            root = root.replace(settings.MEDIA_ROOT+"\\","images/")        
            self.base_cover_name = root

        self.base_cover_ext = ext

        super(ElementImages,self).save(*args, **kwargs)


@receiver(models.signals.post_delete, sender=ElementImages)
def auto_delete_file_on_delete(sender, instance, **kwargs):

    if instance.cover:
        if os.path.isfile(instance.cover.path):
            os.remove(instance.cover.path)
        
    (root, ext) = os.path.splitext(instance.cover.path)
    extra_file = root+".custom.jpeg"

    if os.path.isfile(extra_file):
        os.remove(extra_file)

@receiver(models.signals.pre_save, sender=ElementImages)
def auto_delete_file_on_change(sender, instance, **kwargs):

    if not instance.pk:
        return False

    try:
        old_file = ElementImages.objects.get(pk=instance.pk).cover
    except ElementImages.DoesNotExist:
        return False

    new_file = instance.cover
    if not old_file == new_file:
        if instance.cover:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)

                
        (root, ext) = os.path.splitext(old_file.path)
        extra_file = root+".custom.jpeg"

        if os.path.isfile(extra_file):
            os.remove(extra_file)
