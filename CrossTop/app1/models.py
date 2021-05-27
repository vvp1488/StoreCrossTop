from autoslug import AutoSlugField
from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name='Категория товара')
    slug = models.SlugField(unique=True, help_text='Вводите обязательно английськие буквы без пробелов')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('.html', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'



class Product(models.Model):
    GENDER_MALE = 'male'
    GENDER_FEMALE = 'female'
    GENDER_CHILD = 'child'

    GENDER_CHOICE = (
        (GENDER_MALE, 'Мужские'),
        (GENDER_FEMALE, 'Женские'),
        (GENDER_CHILD, 'Детские')
    )


    id = models.AutoField(primary_key=True)
    slug = AutoSlugField(populate_from='id',unique=True)
    name = models.CharField(max_length=255, verbose_name='Название')
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    brand = models.ForeignKey('Brand', verbose_name='Бренд', on_delete=models.CASCADE)
    gender = models.CharField(max_length=30, verbose_name='Стать', choices=GENDER_CHOICE)
    description = models.TextField(verbose_name='Описание')
    size = models.FloatField(verbose_name='Размер')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата добавления')
    main_photo = models.ImageField(verbose_name='Главное фото')
    season = models.CharField(verbose_name='Сезон',max_length=50,null=True,blank=True)
    in_available = models.BooleanField(default=True)


    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug':self.slug})



    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


    def __str__(self):
        return self.name


class Images(models.Model):
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE,related_name='images')
    image = models.ImageField(verbose_name='Дополнительные фото')


class Brand(models.Model):
    brand_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name='Название бренда')
    slug = models.SlugField(unique=True, null=True, blank=True)
    products = models.ManyToManyField(Product, verbose_name='Товары', blank=True, related_name='related_products')

    def get_absolute_url(self):
        return reverse('.html', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        auto_slug = self.name.lower()
        self.slug = auto_slug
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def __str__(self):
        return self.name


class Customer(models.Model):

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, blank=True, null=True)
    phone = models.CharField(max_length=20, verbose_name='Номер телефона', blank=True, null=True)
    address = models.CharField(max_length=255, verbose_name='Адрес', blank=True, null=True)
    orders = models.ManyToManyField('Order',blank=True, verbose_name='Заказы покупателя', related_name='related_customer')
    anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return 'Покупатель :  {}'.format(self.user)


class CartProduct(models.Model):

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Customer, verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_product')
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    final_price = models.DecimalField(decimal_places=2,max_digits=20,default=0)

    def __str__(self):
        return "Cart Product: {} (для корзины) ".format(self.product.name)


    def save(self,*args,**kwargs):
        self.final_price = self.product.price
        super().save(*args,**kwargs)


class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey('Customer', null=True, verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Общаяя цена')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)





class Order(models.Model):

    STATUS_NEW = 'Новый заказ'
    STATUS_IN_PROGRESS = 'Заказ принят'
    STATUS_READY = 'Заказ готов'
    STATUS_COMPLETED = 'Заказ выполнен'
    DELIVERY_NP = 'Новая почта'
    DELIVERY_UKR = 'Укр почта'
    DELIVERY_INTIME = 'Деливери почта'

    BUYING_TYPE_SELF = 'Самовывоз'
    BUYING_TYPE_DELIVERY = 'Доставка'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Новый заказ'),
        (STATUS_IN_PROGRESS, 'Заказ в обработке'),
        (STATUS_READY, 'Заказ готов'),
        (STATUS_COMPLETED, 'Заказ выполнен')
    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Самовывоз'),
        (BUYING_TYPE_DELIVERY, 'Доставка')

    )
    DELIVERY_CHOICE = (
        (DELIVERY_NP, 'Новая почта'),
        (DELIVERY_UKR, 'Укрпочта'),
        (DELIVERY_INTIME, 'Интайм')
    )
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, verbose_name='Покупатель', on_delete=models.CASCADE,
                                 related_name='related_orders')
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE, null=True, blank=True)
    phone = models.CharField(max_length=25, verbose_name='Телефон')
    address = models.CharField(max_length=1024, verbose_name='Адрес', null=True, blank=True)
    status = models.CharField(max_length=255, verbose_name='Статус заказа', choices=STATUS_CHOICES, default=STATUS_NEW)
    buying_type = models.CharField(
        max_length=255,
        verbose_name='Тип заказа',
        choices=BUYING_TYPE_CHOICES,
        default=BUYING_TYPE_SELF)
    delivery_choice = models.CharField(max_length=100, choices=DELIVERY_CHOICE, default=DELIVERY_NP)
    comment = models.TextField(verbose_name='Коментарий к заказу', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата создания заказа')
    final_price = models.DecimalField(max_digits=20,decimal_places=2,verbose_name='Общая сумма заказа',default=0)



    def __str__(self):
        return f'Дата заказа {self.id} на сумму : {self.final_price} грн'



class NewLogo(models.Model):
    name = models.CharField(max_length=35)
    image = models.ImageField()

    def __str__(self):
        return self.name

