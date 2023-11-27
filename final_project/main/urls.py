from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns =[
    path ('', views.homepage, name='homepage'),
    path ('about/', views.about, name='about'),
    path('products/<int:product_id>/', views.product_detail, name='products'),
    path('get_categories_and_subcategories/', views.get_categories_and_subcategories, name='get_categories_and_subcategories'),
    path('rate_product/', views.rate_product, name='rate_product'),
    path('filter_products/', views.filter_products, name='filter_products'),
    path('search/', views.search_items, name='search_items'),
    # Other URL patterns...
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)