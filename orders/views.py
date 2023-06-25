
from icecream import ic
from django.shortcuts import render, get_object_or_404

# Create your views here.
from  django.views.generic import (
    DetailView,
)
from .forms import (
    OrderCreateForm,
)
from rest_framework import generics, viewsets

from .serializers import OrderSerializer, OrderPaymentSerializer

from cart.services.cart import Cart
from django.db import transaction
from .models import Order, OrderItem

def make_qrr(pk, cart=None):
        import qrcode

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.ERROR_CORRECT_L,
            box_size=10,
            border=4
        )
        qr.add_data(
            {
                'order_url' : f"https://uzumbank.uz/ru/orders/{pk}",
                'order_id' : pk,
                'cart' : cart
            }
            )
        qr.make()
        img = qr.make_image(fill_color ='black', back_color ='white')
        order_id = pk

        img.save(f'media/qrs/order_{order_id}_qr.png')
        return order_id




def commit_handler():
    return 'Transaction done'
# @transaction.atomic
def order_create(request):
    template_name = "pages/orders/order_created.html"
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            form.clean()

        if form.cleaned_data:
            save_point = transaction.savepoint()
            order.user = request.user
            order.email = request.user.email
            order.phone = form.cleaned_data.get('phone')
            order.address = form.cleaned_data.get('address')
            order.postal_code = form.cleaned_data.get('postal_code')
            order.city = form.cleaned_data.get('city')

            try:
                
                order.save()
                transaction.savepoint_commit(save_point)
                

            except:
                transaction.rollback(save_point)
            
            transaction.commit()
            transaction.on_commit(commit_handler)

        for item in cart:
            order_item = OrderItem.objects.create(
                product = item['product'],
                price = item['end_price'],
                quantity = item['quantity'],
                order = order,
            )
        #очистка корзины
        qr  = make_qrr(order.pk, cart)
        cart.clear()
        
        return render(
            request=request, template_name=template_name,context={'order':order, 'qr': qr}
        )
    else:
        
        if request.user.is_authenticated:
            ic('get request')
            form = OrderCreateForm(
                initial={
                    'user':request.user,
                    'first_name':request.user.first_name,
                    'last_name':request.user.last_name,
                    'customer_id' : request.user.pk
                }
            )
        else:
            form = OrderCreateForm()

    return render(
        request, 'pages/orders/order_create.html', {'cart' : cart, 'form' : form}
    )



class OrderPayment(DetailView):
    model = Order
    template_name = 'pages/orders/order_payment.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super(OrderPayment, self).get_context_data(**kwargs)
        context['qr'] = make_qrr(pk = kwargs['object'].pk)

        return context
    

 
class OrderDetailView(DetailView):
    model = Order
    template_name = 'pages/orders/order_detail.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)

        context['order_items'] = OrderItem.items.order_items(kwargs['object'].pk)
        context['order'] = Order.objects.select_related('user').get(
            pk = kwargs['object'].pk
        )
        context['order_price'] = sum(
            [item.price * item.quantity for item in context['order_items']]
        )
        return context



#Orders Api

class OrderAPIView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderPaymentAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderPaymentSerializer
    
    def get(self, request, *args, **kwargs):
        payment = get_object_or_404(Order, pk=kwargs['pk'])
        if kwargs['paid']:
            payment.paid = True
        else:
            payment.paid = False
        payment.save()

        return self.retrieve(request, *args, **kwargs)

        
