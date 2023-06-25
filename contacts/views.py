
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.views.generic import ListView, FormView, DetailView
from django.views.generic.base import TemplateView

from .forms import ContactFormDB
from .models import ContactPage, ContactPageForm



from icecream import ic
# Create your views here.

class ContactPageDetailView(TemplateView):
    template_name = 'contacts/contact_page.html'
    form_class = ContactFormDB
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class
        context['contacts'] = ContactPage.objects.get(pk=1)

        return context

    def post(self, request, *args, **kwargs ):
        template_name = 'contacts/contact_page.html'
        context = self.get_context_data()
        
        form = ContactFormDB(request.POST)
        context['form'] = form
        
        if form.is_valid():
            contact = ContactPageForm()
            data = form.cleaned_data
            contact.email = data.get('email')
            contact.name = data.get('name')
            contact.message = data.get('message')
            contact.subject = data.get('subject')
            contact.save()
            return redirect('contacts:success_contact_message')
        else:
            context['message'] = 'Не правильно заполнены данные'
            return render(request, template_name, context)


class SuccessContactMeassageView(TemplateView):
    template_name = 'contacts/success_contact_meassage.html'
    