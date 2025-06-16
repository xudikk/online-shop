import random

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

from core.models import Category, Product, Cart


def index(request):
    # ctgs = Category.objects.get(id=1)
    most_sale = Product.objects.all()
    try:
        error = request.session.pop("error")
    except:
        error = None

    ctx = {
        "most_sale": most_sale,
        "error": error
    }
    return render(request, 'site/index.html', ctx)


def ctg(request, slug):
    return render(request, 'site/categories.html')


def search(request):
    return render(request, 'site/search.html')


@login_required(login_url='login')
def cart(request, add_id=None):
    if add_id:
        product = Product.objects.filter(id=add_id).first()
        if not product:
            request.session['error'] = "Bunaqa IDlik Mahsulot Topilmadi!"
            return redirect("home")
        print("shu yerda")
        cart = Cart.objects.filter(user=request.user, product=product).first()
        if cart:
            print("bu yerda")
            request.session['error'] = "Bu mahsulot Allaqachon savatga qo`shilgan!"
            return redirect("home")
        print("botta")
        cart = Cart.objects.create(user=request.user, product=product)
        print("cart", cart)
        return redirect("cart")

    carts = Cart.objects.filter(user=request.user)

    ctx = {
        "carts": carts
    }

    return render(request, 'site/cart.html', ctx)


def change_cart(request, cart_id, inc):
    cart = Cart.objects.filter(id=cart_id).first()
    if cart:
        if inc:
            cart.quantity += 1
        else:
            cart.quantity -= 1
        cart.save()
        return JsonResponse({
            "success": "Muaffaqiyatli!",
            "total_balance": request.user.calculate_cart()
        })
    else:
        return JsonResponse({
            "error": "Cart Topilmadi"
        })
