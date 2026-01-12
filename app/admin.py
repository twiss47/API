from django.contrib import admin
from .models import Category, Product, Image


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug", "parent")
    list_filter = ("parent",)
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "price", "is_active", "category")
    list_filter = ("is_active", "category")
    search_fields = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ("price", "is_active")






@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "product", "image")
    list_filter = ("product",)
    search_fields = ("name",)