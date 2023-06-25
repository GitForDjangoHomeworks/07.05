from mainpage.models import NavMenu



def menu_page(request):
    menu = NavMenu.objects.all()
    return {'menu': menu}