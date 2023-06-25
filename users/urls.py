from django.urls import path
from .views import is_user_authenticated

app_name = 'users'
urlpatterns = [
    path('is_user_authenticated', is_user_authenticated, name='is_user_authenticated' )
]