from django.shortcuts import render,get_object_or_404
from .models import products
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

def homepage(request):
    all_products = products.objects.all()
    paginator = Paginator(all_products, 6)  # Display 6 products per page
    page_number = request.GET.get('page')
    try:
        product = paginator.page(page_number)
    except PageNotAnInteger:
        product = paginator.page(1)
    except EmptyPage:
        product = paginator.page(paginator.num_pages)
    return render(request, 'main/home.html', {'products': product})  # Pass 'products' instead of 'all_products'



def product_detail(request, product_id):
    product = get_object_or_404(products, pk=product_id)
    return render(request, 'main/products.html', {'product': product})
