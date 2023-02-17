from pprint import pprint
from addressapp.yandex_geocode import fetch_coordinates

from django import forms
from django.conf import settings
from django.shortcuts import redirect, render
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from geopy import distance

from addressapp.models import AddressCoordinate
from foodcartapp.models import Product, Restaurant, Order, OrderProduct


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
    restaurants = Restaurant.objects.order_by('name')
    products = Product.objects.prefetch_related('menu_items').select_related('category')

    products_with_restaurant_availability = []
    for product in products:
        availability = {item.restaurant_id: item.availability for item in product.menu_items.all()}
        ordered_availability = [availability.get(restaurant.id, False) for restaurant in restaurants]

        products_with_restaurant_availability.append(
            (product, ordered_availability)
        )

    return render(request, template_name="products_list.html", context={
        'products_with_restaurant_availability': products_with_restaurant_availability,
        'restaurants': restaurants,
    })


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_restaurants(request):
    return render(request, template_name="restaurants_list.html", context={
        'restaurants': Restaurant.objects.all(),
    })


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_orders(request):
    orders = Order.objects.exclude(order_status='FN').prefetch_related('products')
    orders_cost_info = OrderProduct.objects.get_order_cost().select_related('order')
    orders_cost = {}
    order_items = []
    for order_cost in orders_cost_info:
        if order_cost.order.id not in orders_cost:
            orders_cost[order_cost.order.id] = order_cost.total_price
        else:
            orders_cost[order_cost.order.id] += order_cost.total_price
    for order in orders:
        addresses = []
        adress_coordinates = {}
        products_in_order = order.products.all()
        products_availability = []
        for product in products_in_order:
            availability = [item.restaurant for item in product.menu_items
                            .filter(availability=True)
                            .select_related('restaurant')]
            products_availability.append(availability)

        restaurants_with_all_products = list(
            set.intersection(*[set(product_restaurants) for product_restaurants in products_availability])
        )
        restaurant_distance = []
        addresses = [restaurant.address for restaurant in restaurants_with_all_products]
        addresses.append(order.address)
        address_objects = AddressCoordinate.objects.filter(address__in=addresses)
        for address in addresses:
            for address_obj in address_objects:
                if address_obj.address == address:
                    adress_coordinates[address] = (address_obj.lat, address_obj.lon)
                    break
            if address not in adress_coordinates.keys():
                lat, lon = fetch_coordinates(settings.YA_GEO_API_KEY, address)
                AddressCoordinate.objects.create(
                    address=address,
                    lat=lat,
                    lon=lon
                )
                adress_coordinates[address] = (lat, lon)

        for restaurant in restaurants_with_all_products:
            user_coord = adress_coordinates[order.address]
            restaurant_coord = adress_coordinates[restaurant.address]

            delivery_distance = round(distance.distance(user_coord, restaurant_coord).km, 3)
            restaurant_distance.append((restaurant, delivery_distance))
        restaurant_distance = sorted(restaurant_distance, key=lambda tpl: tpl[1])
        order_items.append((order, orders_cost[order.id], restaurant_distance))

    return render(request, template_name='order_items.html', context={
        'order_items': order_items
    })
