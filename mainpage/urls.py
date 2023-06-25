from django.urls import path
from .views import MainPageTemplateView
app_name = 'mainpage'
urlpatterns = [
     path('', MainPageTemplateView.as_view(), name='show_mainpage')
]