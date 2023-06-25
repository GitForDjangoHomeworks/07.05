from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
# Create your views here.
from  products.models import SingleProduct
from .services.cart import Cart

from .forms import CartAddProductForm
from icecream import ic


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(SingleProduct, pk=product_id)
    
    form = CartAddProductForm(request.POST)
    # s
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])

    return redirect('products:show_single_product_page', request.POST.get('page_id'))

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(SingleProduct, pk=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    template_name = 'cart/cart_detail.html'
    context = {'cart' : Cart(request)}

    return render(request=request, template_name=template_name, context=context)

def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect('cart:cart_detail')
