from django.contrib import admin

from .models import Message, Coupon

# Register your models here.

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('name','email','element','created','active')
    list_filter = ('active', 'created','updated')
    search_fields = ('name','email','body')

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'valid_from', 'valid_to', 'discount', 'active')
    list_filter = ('active','valid_from', 'valid_to')
    search_fields = ('code',)