from django.urls import path
from .views import(
 ContactPageDetailView,
 SuccessContactMeassageView,
 )
app_name = 'contacts'
urlpatterns = [
    path('', ContactPageDetailView.as_view() , name='contact_page_form_view'),
    path('successful_message', SuccessContactMeassageView.as_view(), name='success_contact_message')
    
]