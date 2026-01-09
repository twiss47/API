from django.db import models

# Create your models here.




    

#================== CATEGORY ==================
class Category(models.Model):
    name = models.CharField(max_length=155)
    slug = models.SlugField(max_length=155)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'

    )

    def __str__(self):
        return self.name
    


#================== PRODUCT ==================

class Product(models.Model):
    title = models.CharField(max_length=155)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products'
    )
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


    def __str__(self):
        return self.title


class Image(models.Model):
    name = models.CharField(max_length=155)
    product = models.ForeignKey(Product, related_name='images',on_delete=models.PROTECT)
    image = models.ImageField(upload_to='product/images')

    def __str__(self):
        return self.name