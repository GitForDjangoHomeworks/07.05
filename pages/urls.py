from django.urls import path
from .views import(

    AllProductsView, 
    add_file,
    get_file,
    index_files,
    delete_file,
)

app_name = 'pages'

urlpatterns = [
    path('all_products', AllProductsView.as_view(), name='all_products'),
    path('add_file',add_file,name = 'add_file'),
    path('files/get/<path:filename>', get_file, name = 'get_file'),
    path('files/',index_files, name='index_files'),
    path('files/delete/<path:filename>', delete_file, name = 'delete_file'),

 ]