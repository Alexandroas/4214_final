from django.contrib import admin
from .models import products, Category, subCategory

class categoryAdmin(admin.ModelAdmin):
    fields = [
        'name',
    ]
    
class subCategoryAdmin(admin.ModelAdmin):
    fields = [
        'name',
    ]    

class productAdmin(admin.ModelAdmin):
    """fieldssets =[  (Add this in the future if things get complicated)
        ("Header"), (https://www.youtube.com/watch?v=ITrRbS95wMs&list=PLbMO9c_jUD44i7AkA4gj1VSKvCFIf59fb&index=5)
        ("Content), (Timestamp:12:00)
        (""), """
    fields =[
        'name',
        'description',
        'price',
        'category',
        'subcategory',
        'image',
    ]

# Register your models here.
admin.site.register(Category, categoryAdmin)
admin.site.register(products, productAdmin)
admin.site.register(subCategory, subCategoryAdmin)