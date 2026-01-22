from django.core.cache import cache

from rest_framework import generics, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, Category, Image
from .serializers import ProductSerializer, CategorySerializer, ImageSerializer
from .permisson import UpdateInLimitedTime


# -------------------------
# Pagination
# -------------------------
class HundredPagination(PageNumberPagination):
    page_size = 100


# -------------------------
# Product ViewSet (CACHE #1)
# -------------------------
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [UpdateInLimitedTime]
    pagination_class = HundredPagination

    def get_queryset(self):
        return (
            Product.objects
            .select_related('category')
            .prefetch_related('images')
            .order_by('-id')
        )

    def list(self, request, *args, **kwargs):
        page = request.query_params.get('page', 1)
        cache_key = f'products:list:page:{page}'

        cached = cache.get(cache_key)
        if cached is not None:
            return Response(cached)

        queryset = self.filter_queryset(self.get_queryset())

        page_qs = self.paginate_queryset(queryset)
        if page_qs is not None:
            serializer = self.get_serializer(page_qs, many=True)
            response = self.get_paginated_response(serializer.data)
            cache.set(cache_key, response.data, timeout=60)
            return response

        serializer = self.get_serializer(queryset, many=True)
        cache.set(cache_key, serializer.data, timeout=60)
        return Response(serializer.data)


# -------------------------------------------
# Products by child category slug (CACHE #2)
# -------------------------------------------
class ProductListByChildCategorySlugAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    pagination_class = HundredPagination

    def get_queryset(self):
        slug = self.kwargs['slug']
        return (
            Product.objects.filter(
                category__slug=slug,
                category__parent__isnull=False,
                is_active=True,
            )
            .select_related('category')
            .prefetch_related('images')
            .order_by('price')
        )

    def list(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        page = request.query_params.get('page', 1)

        cache_key = f'products:child_category:{slug}:page:{page}'
        cached = cache.get(cache_key)
        if cached is not None:
            return Response(cached)

        queryset = self.filter_queryset(self.get_queryset())

        page_qs = self.paginate_queryset(queryset)
        if page_qs is not None:
            serializer = self.get_serializer(page_qs, many=True)
            response = self.get_paginated_response(serializer.data)
            cache.set(cache_key, response.data, timeout=60)
            return response

        serializer = self.get_serializer(queryset, many=True)
        cache.set(cache_key, serializer.data, timeout=60)
        return Response(serializer.data)


# -------------------------
# Category detail
# -------------------------
class CategoryDetailAPIView(generics.RetrieveAPIView):
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'

    def get_queryset(self):
        return Category.objects.all().prefetch_related('products')


# -------------------------
# Category list (CACHE #3)
# -------------------------
class CategoryListAPIView(generics.ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Category.objects.all().prefetch_related('products').order_by('-id')

    def list(self, request, *args, **kwargs):
        cache_key = 'categories:list'
        cached = cache.get(cache_key)

        if cached is not None:
            return Response(cached)

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        cache.set(cache_key, serializer.data, timeout=60 * 5)
        return Response(serializer.data)


# -------------------------
# Image list (BONUS cache)
# -------------------------
class ImageListApiView(generics.ListAPIView):
    serializer_class = ImageSerializer
    permission_classes = [AllowAny]
    pagination_class = HundredPagination

    def get_queryset(self):
        return Image.objects.select_related('product').order_by('-id')

    def list(self, request, *args, **kwargs):
        page = request.query_params.get('page', 1)
        cache_key = f'images:list:page:{page}'

        cached = cache.get(cache_key)
        if cached is not None:
            return Response(cached)

        queryset = self.filter_queryset(self.get_queryset())

        page_qs = self.paginate_queryset(queryset)
        if page_qs is not None:
            serializer = self.get_serializer(page_qs, many=True)
            response = self.get_paginated_response(serializer.data)
            cache.set(cache_key, response.data, timeout=60 * 2)
            return response

        serializer = self.get_serializer(queryset, many=True)
        cache.set(cache_key, serializer.data, timeout=60 * 2)
        return Response(serializer.data)


# -------------------------
# Auth views
# -------------------------
class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        return Response({'detail': 'Logged out successfully'})


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            'username': request.user.username,
            'id': request.user.id
        })
