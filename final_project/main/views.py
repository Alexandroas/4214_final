from django.http import JsonResponse
from django.shortcuts import render,get_object_or_404
from .models import products, subCategory, Category, Rating
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.db.models import Q

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


def get_categories_and_subcategories(request):
    categories = Category.objects.all()
    subcategories = subCategory.objects.all()

    category_list = [{'id': category.id, 'name': category.name} for category in categories]
    subcategory_list = [{'id': subcategory.id, 'name': subcategory.name} for subcategory in subcategories]

    return JsonResponse({'categories': category_list, 'subcategories': subcategory_list})

def filter_products(request):
    category_id = request.GET.get('category')
    subcategory_id = request.GET.get('subcategory')

    productss = products.objects.all()

    if category_id:
        productss = productss.filter(category_id=category_id)
    if subcategory_id:
        productss = productss.filter(subcategory_id=subcategory_id)

        products_list = [
        {
            'name': product.name,
            'category': product.category.name if product.category else None,
            'subcategory': product.subcategory.name if product.subcategory else None,
            'price': product.price,
            'image_url': product.image.url if product.image else None
            # Include other attributes as needed
        }
        for product in productss
    ]

    return JsonResponse({'products': products_list})

def rate_product(request):
    if request.method == 'POST' and request.user.is_authenticated:
        product_id = request.POST.get('product_id')
        stars = request.POST.get('stars')

        # Save the rating for the product by the authenticated user
        Rating.objects.create(product_id=product_id, user=request.user, stars=stars)

        return JsonResponse({'message': 'Rating saved successfully!'})
    else:
        return JsonResponse({'error': 'Invalid request or user not authenticated.'}, status=400)
    
def search_items(request): #search view to search products based on name or category
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    if query:
        # Perform case-insensitive and approximate search on name and category
        items = products.objects.filter(
            Q(name__icontains=query) | Q(category__id=category_id)
        )
    else:
        items = products.objects.none()  # Return an empty queryset if no query provided

    return render(request, 'main/search_results.html', {'items': items, 'query': query})
