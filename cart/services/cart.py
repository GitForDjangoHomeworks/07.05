from decimal import Decimal
from django.conf import settings
from products.models import SingleProduct
from icecream import ic 
class Cart(object):
    def __init__(self,request) -> None:
        '''

        Initialization of cart

        '''
        
        self.session = request.session
 

        cart = self.session.get(settings.CART_SESSION_ID)
      

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart
      
    def add(self, product, quantity=1, update_quantity = False):

        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity' : 0, 'end_price' : str(product.end_price)}

        if update_quantity:
            self.cart[product_id]['quantity'] = int(quantity)
        else:
            self.cart[product_id]['quantity'] += int(quantity)
        self.save()

    def save(self):

        self.session[settings.CART_SESSION_ID] = self.cart

        self.session.modified = True

    def remove(self, product):

        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()

        products = SingleProduct.objects.prefetch_related("images").filter(id__in=product_ids)

        for product in products:
            self.cart[str(product.pk)] ['product'] = product
        ic(self.cart)
        for item in self.cart.values():
            item['end_price'] = Decimal(item['end_price'])
            item['total_price'] = item['end_price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())


    def get_total_price(self):

        return sum(
            Decimal( item['end_price']) * item['quantity'] for item in self.cart.values() )
        

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
