from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ProductViewSet, ProductListByChildCategorySlugAPIView



router = DefaultRouter()
router.register(r"", ProductViewSet, basename='product')

urlpatterns = [
    path("", include(router.urls)),

    path(
        "products/by-child-category/<slug:slug>/",
        ProductListByChildCategorySlugAPIView.as_view(),
        name="product-list-by-child-category-slug",
    ),
    
]


