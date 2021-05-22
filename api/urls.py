from django.urls import path
from .views import speedometer, get_price_data, get_predicted_prices

urlpatterns = [
    path('price-change', speedometer),
    path('price-data', get_price_data),
    path('predicted-price', get_predicted_prices)
]
