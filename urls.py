"""Django urls module."""
from django.urls import path
from .views import city_map, update_layers

app_name = "maps"

urlpatterns = [
    path("", city_map, name="city_map"),
    path("update_layers/", update_layers, name="update_layers"),
]
