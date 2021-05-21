from django.urls import path
from .views import speedometer

urlpatterns = [
    path('price-change', speedometer)
]
