from rest_framework import serializers
from .models import Product, Category, Image



class ImageSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source = 'product.title')
    class Meta:
        model = Image
        exclude = ()


class ProductMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "title", "slug", "price"]


class CategorySerializer(serializers.ModelSerializer):
    products = ProductMiniSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name", "slug",'products']



class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    category_id = serializers.PrimaryKeyRelatedField(
        source="category",
        queryset=Category.objects.all(),
        write_only=True
    )

    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "price",
            "is_active",
            "category",     
            "category_id",  
            "images",
            "created_at",
            "updated_at",
        ]



class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name", "slug",'products']
