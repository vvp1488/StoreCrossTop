from django.views.generic.detail import SingleObjectMixin
from django.views.generic import View
from .models import *
from django.contrib.auth import get_user_model
from.filters import NavbarFilter

User = get_user_model()

class BaseMixin():
    categories = Category.objects.all()
    products = Product.objects.all()
    brands = Brand.objects.all()

class CartMixin(View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            customer = Customer.objects.filter(user=request.user).first()
            cart_products = CartProduct.objects.filter(user=customer)
            if not customer:
                customer = Customer.objects.create(user=request.user)
            cart = Cart.objects.filter(owner=customer, in_order=False).first()
            if not cart:
                cart = Cart.objects.create(owner=customer)


        else:
            cart_products = None

            cart = Cart.objects.filter(for_anonymous_user=True).first()
            customer = None
        if not cart:
            cart = Cart.objects.create(for_anonymous_user=True)

        self.cart = cart
        self.cart_products = cart_products
        self.customer = customer
        self.navbar_filter = NavbarFilter(self.request.GET, queryset=Product.objects.all())

        return super().dispatch(request,*args,**kwargs)