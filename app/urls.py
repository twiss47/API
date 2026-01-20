from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ProductViewSet,
    ProductListByChildCategorySlugAPIView,
    CategoryDetailAPIView,
    LogoutView,
    MeView,
    ImageListApiView,
)

router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="product")


urlpatterns = [
    path("", include(router.urls)),
    path("categories/<slug:slug>/",CategoryDetailAPIView.as_view(),name="category-detail",),
    path("products/by-child-category/<slug:slug>/",ProductListByChildCategorySlugAPIView.as_view(),name="products-by-child-category",),
    path("images/",ImageListApiView.as_view(),name="image-list",),
    path("logout/",LogoutView.as_view(),name="logout",),
    path("me/",MeView.as_view(),name="me",),
]
