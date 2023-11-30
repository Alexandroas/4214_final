from django.db import models
from django.db.models import Avg
from tinymce.models import HTMLField
from django.utils.text import slugify
import uuid
from django.contrib.auth import get_user_model

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class subCategory(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class products(models.Model):
    name = models.CharField(max_length=100)
    description = HTMLField(blank=True, default="")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(subCategory, on_delete=models.CASCADE, null=True, blank=True)
    product_slug = models.SlugField("Product Slug", null=False, blank=False, unique=True)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    
    def average_rating(self) -> float:
        return Rating.objects.filter(product=self).aggregate(Avg("rating"))["rating__avg"] or 0
    
    def __str__(self):
        return f"{self.name}: {self.average_rating()}"
    class Meta:
        ordering=['price']
        
    def save(self, *args, **kwargs):
        # If the product doesn't have a slug or is being updated
        if not self.product_slug or self._state.adding:
            # Generate a unique identifier (UUID)
            unique_id = uuid.uuid4().hex[:8]  # Use the first 8 characters of the UUID
            # Create a slug based on the product's name and the unique identifier
            self.product_slug = slugify(self.name + '-' + unique_id)
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
        
class Rating(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    product = models.ForeignKey(products, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.name}: {self.rating}"