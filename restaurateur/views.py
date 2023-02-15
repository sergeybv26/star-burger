from pprint import pprint

import requests
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


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lat, lon


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_orders(request):
    orders = Order.objects.exclude(order_status='FN').prefetch_related('products')

    products_in_restaurants = {}
    restaurants_coordinates = {}
    orders_cost = {}
    for order in orders:
        products_in_order = order.products.all()
        order_cost = OrderProduct.objects.get_order_cost(order)
        orders_cost[order.id] = order_cost.total_price
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
        for restaurant in restaurants_with_all_products:
            try:
                address_obj = AddressCoordinate.objects.get(address=order.address)
                user_coord = (address_obj.lat, address_obj.lon)
            except AddressCoordinate.DoesNotExist:
                user_coord = fetch_coordinates(settings.YA_GEO_API_KEY, order.address)
                if not user_coord:
                    continue
                AddressCoordinate.objects.create(
                    address=order.address,
                    lat=user_coord[0],
                    lon=user_coord[1]
                )
            if restaurant not in restaurants_coordinates.keys():
                try:
                    address_obj = AddressCoordinate.objects.get(address=restaurant.address)
                    restaurant_coord = (address_obj.lat, address_obj.lon)
                except AddressCoordinate.DoesNotExist:
                    restaurant_coord = fetch_coordinates(settings.YA_GEO_API_KEY, restaurant.address)
                    if not restaurant_coord:
                        continue
                    AddressCoordinate.objects.create(
                        address=restaurant.address,
                        lat=restaurant_coord[0],
                        lon=restaurant_coord[1]
                    )
                restaurants_coordinates[restaurant] = restaurant_coord
            else:
                restaurant_coord = restaurants_coordinates[restaurant]

            delivery_distance = round(distance.distance(user_coord, restaurant_coord).km, 3)
            restaurant_distance.append((restaurant, delivery_distance))
        restaurant_distance = sorted(restaurant_distance, key=lambda tpl: tpl[1])
        products_in_restaurants[order.id] = restaurant_distance

    return render(request, template_name='order_items.html', context={
        'order_items': orders,
        'orders_cost': orders_cost,
        'restaurants': products_in_restaurants
    })
