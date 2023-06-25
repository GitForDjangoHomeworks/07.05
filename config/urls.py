"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mainpage.urls', namespace='mainpage.mainpage')),
    path('products/', include('products.urls', namespace='products.products')),
    path('contacts/', include('contacts.urls', namespace='contacts.contacts')),
    path('cart/', include('cart.urls', namespace='cart.cart')),\
    path('orders/', include('orders.urls', namespace='orders.orders')),
    path('users/', include('users.urls', namespace='users.users')),
    path('pages/', include('pages.urls', namespace='pages.pages')),
    #USERS
    path('accounts/login', LoginView.as_view(template_name='users/registration/login.html'), name='login'),
    path('accounts/logout', LogoutView.as_view(template_name='users/registration/logout.html'), name='logout'),
    #CAPTCHA
    path('captcha/', include('captcha.urls'))
]


urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)