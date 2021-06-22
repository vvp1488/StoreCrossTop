import django_filters
from django.forms import TextInput

from .models import Product, Brand


class NavbarFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(field_name='name',lookup_expr='icontains', widget=TextInput(attrs={'placeholder': 'Поиск по названию','size':'40'}))

    class Meta:
        model=Product
        fields = ()


class ProductFilter(django_filters.FilterSet):

    qs_for_brand = Brand.objects.all()
    qs_for_filter = Product.objects.order_by('size')
    CHOICES_FOR_SIZE = []
    for item in qs_for_filter:
        if not (item.size,item.size) in CHOICES_FOR_SIZE:
            CHOICES_FOR_SIZE.append((item.size,item.size))

    CHOICES_FOR_BRAND = [(item.brand_id, item.name) for item in qs_for_brand]


    CHOICES_FOR_GENDER = (
        ('man', 'Мужские'),
        ('woman', 'Женские'),
        ('kid', 'Детские')

    )
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains',widget=TextInput(attrs={'placeholder': 'Поиск по названию','size':'40'}))
    filter_by_gender = django_filters.ChoiceFilter(label='Пол', choices=CHOICES_FOR_GENDER, method='filter_for_gender')
    filter_by_brand = django_filters.ChoiceFilter(label='Бренд',field_name='brand', choices=CHOICES_FOR_BRAND)
    filter_by_size = django_filters.ChoiceFilter(label='Размер',field_name='size', choices=CHOICES_FOR_SIZE)



    class Meta:
        model = Product
        fields = {}

    def order_by_exp_first(self):
        return self.queryset.order_by('price')

    def order_by_cheap_first(self):
        return self.queryset.order_by('-price')





    def filter_for_gender(self, queryset, name, value):
        if value == 'man':
            return queryset.filter(gender='male')
        elif value == 'woman':
            return queryset.filter(gender='female')
        elif value == 'kid':
            return queryset.filter(gender='child')
        return queryset


