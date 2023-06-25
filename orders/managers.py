from django.db import models

class OrderItemQueruySet(models.QuerySet):
    def order_items(self, pk):
        return self.select_related('order', 'product').filter(order_id=pk)

class OrderItemManager(models.Manager):
    def get_queryset(self) -> OrderItemQueruySet:
        return OrderItemQueruySet(self.model)

    def order_items(self, pk ):
        return self.get_queryset().order_items(pk)