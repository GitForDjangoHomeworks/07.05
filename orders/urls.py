from email.mime import base
from django.urls import path

from orders.models import Order
from .views import OrderPayment, order_create, OrderDetailView, OrderAPIView, OrderPaymentAPIView
from rest_framework.routers import DefaultRouter
app_name = 'orders'
router = DefaultRouter()
router.register('payment', OrderAPIView, basename='payment')

urlpatterns = [
    path('create/', order_create, name='order_create'),
    path('<int:pk>/qr/', OrderPayment.as_view(), name='order_qr'),
    path('<int:pk>/detail/', OrderDetailView.as_view(), name='order_detail'),
    # Payment
    path('<int:pk>/paid/<int:paid>', OrderPaymentAPIView.as_view(), name='paid')
]
urlpatterns += router.urls
