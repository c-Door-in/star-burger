from django import forms
from django.shortcuts import redirect, render
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test

from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from django.db.models import Count


from foodcartapp.models import Product, Restaurant, Order, RestaurantMenuItem, OrderItem


class Login(forms.Form):
    username = forms.CharField(
        label='Логин', max_length=75, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Укажите имя пользователя'
        })
    )
    password = forms.CharField(
        label='Пароль', max_length=75, required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = Login()
        return render(request, "login.html", context={
            'form': form
        })

    def post(self, request):
        form = Login(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if user.is_staff:  # FIXME replace with specific permission
                    return redirect("restaurateur:RestaurantView")
                return redirect("start_page")

        return render(request, "login.html", context={
            'form': form,
            'ivalid': True,
        })


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('restaurateur:login')


def is_manager(user):
    return user.is_staff  # FIXME replace with specific permission


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_products(request):
    restaurants = list(Restaurant.objects.order_by('name'))
    products = list(Product.objects.prefetch_related('menu_items'))

    default_availability = {restaurant.id: False for restaurant in restaurants}
    products_with_restaurants = []
    for product in products:

        availability = {
            **default_availability,
            **{item.restaurant_id: item.availability for item in product.menu_items.all()},
        }
        orderer_availability = [availability[restaurant.id] for restaurant in restaurants]

        products_with_restaurants.append(
            (product, orderer_availability)
        )

    return render(request, template_name="products_list.html", context={
        'products_with_restaurants': products_with_restaurants,
        'restaurants': restaurants,
    })


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_restaurants(request):
    return render(request, template_name="restaurants_list.html", context={
        'restaurants': Restaurant.objects.all(),
    })


def get_restaurant_details(order, menu_items):
    if order.restaurant:
        return (f'Готовит {order.restaurant.name}', None)

    order_products = (order.order_items.all().values_list('product'))
    order_restaurants = (
        menu_items
        .filter(product__in=order_products)
        .values('restaurant')
        .annotate(products_count=Count('product'))
        .filter(products_count=order_products.count())
        .values_list('restaurant')
    )
    if order_restaurants:
        return (
            'Может быть приготовлен ресторанами:',
            Restaurant.objects.filter(pk__in=order_restaurants),
        )

    return ('Ошибка определения координат', None)


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_orders(request):
    orders = (
        Order.objects
        .select_related('restaurant')
        .prefetch_related('order_items')
        .order_with_cost()
        .exclude(status='3')
        .order_by('restaurant', 'created_at')
    )
    menu_items = RestaurantMenuItem.objects.select_related('restaurant')\
                                           .select_related('product')

    orders_with_restaurants = []
    for order in orders:
        summary, restaurants = get_restaurant_details(order, menu_items)
        orders_with_restaurants.append(
            (order, summary, restaurants)
        )
    print(orders_with_restaurants)
    return render(request, template_name='order_items.html', context={
        'orders_with_restaurants': orders_with_restaurants,
    })
