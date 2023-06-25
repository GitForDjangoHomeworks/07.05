from django import template

from django.utils.safestring import mark_safe
from django.utils.html import escape

from django.conf import settings

from mainpage.models import FooterAbout, Social, NavMenu
from contacts.models import ContactPage
from cart.services.cart import Cart
from mainpage.models import Brands

from icecream import ic 

register = template.Library()

@register.filter(needs_autoescape=True)
def lower(value, autoescape=True):
    if autoescape:
        value = escape(value)
    return value.lower()

@register.simple_tag
def footer_about_title():
    title = FooterAbout.title.objects.prefetch_related("social", "menu").get(pk=1).title
    return f'{title}'

@register.simple_tag
def footer_about_text():
    text = FooterAbout.title.objects.prefetch_related("social", "menu").get(pk=1).text
    return f'{text}'

@register.simple_tag
def footer_social():
    social_items = Social.objects.all()
    social_block = f"""
        {"".join(f'<a href="{item.url}"><i class="{item.icon_class}"></i></a>' for item in social_items)}

    """
    return mark_safe(social_block)

@register.inclusion_tag('tags/footer_part_menu.html')
def footer_part_menu(title,*args):
    return {'items' : args,
            'title' : title}

@register.inclusion_tag('tags/footer_contact.html')
def footer_contact():
    contact = ContactPage.objects.get(pk=1)
    return {
        'contact' : contact,
    }

@register.simple_tag(name='number_products_in_cart', takes_context=True)
def number_products_in_cart():
    # cart = Cart(settings.CART_SESSION_ID)
    cart = Cart.session.get(settings.CART_SESSION_ID)
    
    num = len(cart)
    return num

@register.inclusion_tag('tags/nav_menu.html')
def nav_menu():
    nav_items = NavMenu.objects.all()
    return {
        'nav_items' : nav_items,
    }
    
@register.inclusion_tag('tags/mainpage_brands.html')
def mainpage_brands():
    args = Brands.objects.all()
    return {
        'brand_items' : args,
    }