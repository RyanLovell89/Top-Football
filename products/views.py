from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.db.models.functions import Lower
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category
from .forms import ProductsForm

# Create your views here.


def all_products(request):

    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You need to enter a search criteria")
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)


def product_information(request, product_id):

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_information.html', context)


def add_product_to_store(request):

    if request.method == 'POST':
        form = ProductsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Success!, Product has been added to the store.')

            return redirect(reverse('add_product_to_store'))
        else:
            messages.error(request, 'Error!, Product was not added to store, please check the form.')
    else:
        form = ProductsForm()

    template = 'products/add_products.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


def edit_product_on_store(request, product_id):

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductsForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Success! The product has been updated.')
            return redirect(reverse('product_information', args=[product.id]))
        else:
            messages.error(request, 'Error! The product was not updated, please check the form')
    else:
        form = ProductsForm(instance=product)
        messages.info(request, f'{product.name} is being edited')

    template = 'products/edit_products.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)
