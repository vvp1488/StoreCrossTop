from django.shortcuts import render
from django.views.generic import View, DetailView
from .models import Product, Category, Images, CartProduct, Cart, Customer ,Order
from django.http import HttpResponseRedirect
from .forms import OrderForm ,LoginForm, RegistrationForm
from .mixins import BaseMixin, CartMixin
from .utils import recalc_cart
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model

User = get_user_model()

#
from .utils import recalc_cart


class BaseView(BaseMixin, CartMixin, View):

    def get(self, request, *args, **kwargs):
        context = {
            'products': self.products,
            'categories': self.categories,
            'cart': self.cart,
            'logo': self.logo,
            'brands' : self.brands,


        }
        return render(request, 'base.html', context)


class DetailProductView(BaseMixin, CartMixin, DetailView):
    queryset = Product.objects.all()

    context_object_name = 'product'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logo'] = self.logo
        context['categories'] = self.categories
        context['logo1'] = self.logo1
        context['logo2'] = self.logo2
        context['cart'] = self.cart
        context['brands'] =self.brands
        return context

    # def post(self,request,*args,**kwargs):
    #
    #     product_pk = kwargs.get('pk')
    #     return HttpResponseRedirect('/')


class AddToCartView(BaseMixin, CartMixin, View):

    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        product = Product.objects.get(slug=slug)
        if request.user.is_authenticated:
            current_customer = Customer.objects.get(user=request.user)
            cart_product, created = CartProduct.objects.get_or_create(
            user=current_customer, cart=self.cart, product=product
        )
            if created:
                self.cart.products.add(cart_product)
                recalc_cart(self.cart)
            recalc_cart(self.cart)
            messages.add_message(request, messages.INFO, 'Товар успешно добавлен в корзину')
            return HttpResponseRedirect('/cart/')
        else:
            messages.add_message(request,messages.INFO,'Для покупки нужно сначала войти в личный кабинет')
        return HttpResponseRedirect('/login/')


class DeleteFromCartView(BaseMixin, CartMixin, View):

    def get(self, request, *args, **kwargs):
        product = Product.objects.get(slug=kwargs.get('slug'))
        cart_product = CartProduct.objects.get(product=product,cart=self.cart)
        # print(cart_product)
        cart_product.delete()
        recalc_cart(self.cart)

        messages.add_message(request, messages.WARNING, 'Товар успешно убран из корзины')
        return HttpResponseRedirect('/cart/')


class CartView(BaseMixin, CartMixin, View):

    def get(self, request, *args, **kwargs):

        context = {
            'logo': self.logo,

            'cart': self.cart,
            'categories': self.categories,
            'cart_products': self.cart_products,
            'brands': self.brands

        }
        return render(request, 'cart.html', context)


class CheckOutView(BaseMixin, CartMixin, View):

    def get(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)

        context = {
            'form': form,
            'cart': self.cart,
            'categories': self.categories,
            'cart_products': self.cart_products,
            'logo':self.logo,
            'brands': self.brands
        }
        return render(request, 'check_out.html', context)

    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        customer = Customer.objects.filter(user=request.user).first()

        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.delivery_type = form.cleaned_data['buying_type']
            new_order.delivery_choice = form.cleaned_data['delivery_choice']
            new_order.comment = form.cleaned_data['comment']
            new_order.customer_id = customer.pk
            new_order.final_price = self.cart.final_price

            #
            # for item in self.cart_products:
            #     new_order.products.add(item)
            #     item.delete()
            new_order.save()
            self.cart.in_order = True
            self.cart.save()
            new_order.cart = self.cart
            new_order.save()

            customer.orders.add(new_order)
            messages.add_message(request, messages.INFO, 'Заказ успешно оформлен,ожидайте - менеджер с вами ссвяжеться')

            return HttpResponseRedirect('/')
        messages.add_message(request, messages.INFO, 'Форма заполнена не правильно')
        return HttpResponseRedirect('/check-out/')


class CategoryDetailView(BaseMixin,CartMixin,View):

    def get(self,request,*args,**kwargs):

        category = Category.objects.get(slug=kwargs.get('slug'))
        products = Product.objects.filter(category=category)
        context = {
            'products' : products,
            'logo' :self.logo,
            'categories':self.categories,
            'brands': self.brands,
            'category': category

        }
        return render(request,'products_by_category.html',context)


class LoginView(BaseMixin,CartMixin, View):

    def get(self,request,*args,**kwargs):
        form = LoginForm(request.POST or None)
        context = {
            'categories': self.categories,
            'form' : form,
            'cart': self.cart,
            'logo': self.logo
        }
        return render(request,'login.html',context)

    def post(self,request,*args,**kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username,password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        context = {
            'form':form,
            'categories': self.categories,
            'logo': self.logo,
            'cart': self.cart,

        }
        return render(request,'login.html',context)



class RegistrationView(BaseMixin,CartMixin,View):
    def get(self,request,*args,**kwargs):
        form = RegistrationForm(request.POST or None)
        context = {
            'form': form,
            'categories': self.categories,
            'cart': self.cart,
            'logo': self.logo,
            'brands': self.brands
        }
        return render(request,'registration.html',context)

    def post(self,request,*args,**kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Customer.objects.create(
                user=new_user,
                phone=form.cleaned_data['phone']
            )
            user = authenticate(
                username=new_user.username, password=form.cleaned_data['password']
            )
            login(request, user)
            messages.add_message(request,messages.INFO,f'Пользователь {new_user.username} успешно зарегестрирован!')
            return HttpResponseRedirect('/')
        context = {
            'form':form,
            'categories':self.categories,
            'cart':self.cart,
            'logo':self.logo,
            'brands':self.brands,
        }
        return render(request, 'registration.html', context)


class ProfileView(BaseMixin,CartMixin,View):

    def get(self,request,*args,**kwargs):
        orders = Order.objects.filter(customer=self.customer)
        context = {
            'orders' : orders,
            'logo':self.logo,
            'categories':self.categories,
            'brands': self.brands,
            'cart':self.cart
        }
        return render(request,'profile.html',context)

