from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ProductViewSet,
    ProductListByChildCategorySlugAPIView,
    CategoryDetailAPIView,
    LogoutView
)

router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="product")

urlpatterns = [
    path("", include(router.urls)),
    path("categories/<slug:slug>/", CategoryDetailAPIView.as_view(), name="category-detail"),
    path(
        "products/by-child-category/<slug:slug>/",
        ProductListByChildCategorySlugAPIView.as_view(),
        name="product-list-by-child-category-slug",
    ),
    path("api/logout/", LogoutView.as_view(), name="logout"),
]
