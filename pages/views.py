import os
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from products.models import SingleProduct
from .forms import AddFileForm
from datetime import datetime
from pathlib import Path
from django.conf import settings
from icecream import ic
# Create your views here.

class AllProductsView(TemplateView):
    template_name = 'pages/show_page/all_products.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = SingleProduct.objects.prefetch_related('images')
        return context

def add_file(request):
    if request.method == 'POST':
        form = AddFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            ic(uploaded_file)
            
            file_name = f"{datetime.now().timestamp()}{os.path.splitext(uploaded_file.name)[1]}"
            
            file_with_path = Path(settings.FILES_ROOT, file_name)
       
            with open(file_with_path, 'wb') as destination:
                ic(destination)
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            redirect ('pages:index_files')
    else:
        form = AddFileForm()
    context = {'form' : form}
    template_name = "pages/files/add_file.html"

    return render(request, template_name=template_name, context=context)

def get_file(request, filename):
    from django.http import FileResponse
    fn = Path(settings.FILES_ROOT, filename)
    return FileResponse(open(fn, 'rb'), content_type='application/ostet-stream')

def index_files(request):
    template_name = "pages/files/indexx.html"
    files = []
    ic(os.scandir(settings.FILES_ROOT))
    for entry in os.scandir(settings.FILES_ROOT):
        ic(entry)
        files.append(os.path.basename(entry))

    if not files: 
        no_files = 'Файлов нет'
        context = {'no_file' : no_files}
    else:
        context = {'files' : files}
    return render(request, template_name, context=context)

def delete_file(request, filename):
    fn = Path(settings.FILES_ROOT, filename)
    ic(fn)
    os.remove(fn)

    return redirect('pages:index_files')
