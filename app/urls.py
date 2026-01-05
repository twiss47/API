from django.urls import path
from .views_cbv import CarListCreateView, CarDetailView
from .views import car_detail_update_delete, car_list_create

urlpatterns = [
    path("", CarListCreateView.as_view(), name="car-list-create"),
    path("cars/<int:pk>/", CarDetailView.as_view(), name="car-detail"),
    path("cars/", car_list_create, name="car-list-create"),
    path("cars/<int:pk>/", car_detail_update_delete, name="car-detail"),
]


