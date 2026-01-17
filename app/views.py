from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from .permisson import UpdateInLimitedTime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token



class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [UpdateInLimitedTime]

    def get_queryset(self):
        return (
            Product.objects.all()
            .select_related('category')
            .prefetch_related('images')   
        )


class ProductListByChildCategorySlugAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

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


class CategoryDetailAPIView(generics.RetrieveAPIView):
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"
    queryset = Category.objects.all()




class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        return Response({"detail": "Logged out successfully"})