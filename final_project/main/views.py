from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render,get_object_or_404
from .models import Rating, products, subCategory, Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.db.models import Q

def homepage(request):
    all_products = products.objects.all()
    paginator = Paginator(all_products, 8)  # Display 8 products per page
    page_number = request.GET.get('page')
    try:
        product = paginator.page(page_number)
    except PageNotAnInteger:
        product = paginator.page(1)
    except EmptyPage:
        product = paginator.page(paginator.num_pages)
    return render(request, 'main/home.html', {'products': product})

def about(request):
    return render(request, "main/about.html")


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
        products_list = [
        {
            'name': product.name,
            'category': product.category.name if product.category else None,
            'subcategory': product.subcategory.name if product.subcategory else None,
            'price': product.price, #i know repeating code is not a good practise
            'image_url': product.image.url if product.image else None
            # Include other attributes as needed
        }
        for product in productss
    ]
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

def index(request: HttpRequest) -> HttpResponse:
    productss = products.objects.all()
    for Product in productss:
        rating = Rating.objects.filter(product=Product, user=request.user).first()
        Product.user_rating = rating.rating if rating else 0
    return render(request, "main/home.html", {"productss": productss})

def rate(request: HttpRequest, products_id: int, rating: int) -> HttpResponse:
    products_obj = products.objects.get(id=products_id)
    Rating.objects.filter(product=products_obj, user=request.user).delete()
    products_obj.rating_set.create(user=request.user, rating=rating)
    return index(request)
