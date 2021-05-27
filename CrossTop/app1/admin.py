from django.contrib import admin
from .models import *
# Register your models here.


class BrandAdmin(admin.ModelAdmin):
    fields = ('name','products')
    list_display = ('name','slug')


class ProductImagesInline(admin.StackedInline):
    model = Images
    extra = 5


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesInline]
    list_display = ('name','created_at','id','slug')

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id','user')

class CartAdmin(admin.ModelAdmin):
    list_display = ('id','owner')

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(CartProduct)
admin.site.register(Cart,CartAdmin)
admin.site.register(Customer,CustomerAdmin)
admin.site.register(Order)
admin.site.register(Brand,BrandAdmin)

admin.site.register(NewLogo)