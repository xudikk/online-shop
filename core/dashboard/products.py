from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from core.models import Product, Category, Brand
from .forms import ProductForm


def list(request):
    prods = Product.objects.all()

    paginator = Paginator(prods, settings.LIST_PER_PAGE)
    page = request.GET.get('page', 1)
    result = paginator.get_page(page)

    ctx = {
        "result": result,
        "paginator": paginator,
        "page_number": int(page),
        'status': 'list'
    }
    return render(request, "dashboard/pages/product.html", ctx)


def info(request, pk):
    obj = Product.objects.filter(id=pk).first()
    if not obj:
        return render(request, 'dashboard/pages/product.html', {'error': 404})

    ctx = {
        "status": "detail",
        "obj": obj
    }
    return render(request, 'dashboard/pages/product.html', ctx)


def form(request, pk=None):  # edit, add
    obj = None
    if pk:
        obj = Product.objects.filter(id=pk).first()
        if not obj:
            return render(request,  'dashboard/pages/product.html', {"error": 404})
    form = ProductForm(instance=obj)
    print(form)
    if request.POST:
        form = ProductForm(request.POST, request.FILES or None, instance=obj)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
        return redirect('prod-list')

    ctx = {
        "status": "form",
        "categories": Category.objects.all(),
        "brands": Brand.objects.all(),
        'obj': obj,
    }
    return render(request, 'dashboard/pages/product.html', ctx)






