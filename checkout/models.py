import uuid
from django.db import models
from django.db.models import Sum
from django.conf import settings
from products.models import Product


# Create your models here.


class OrderInformation(models.Model):

    class Meta:
        verbose_name_plural = 'Order Information'

    order_number = models.CharField(max_length=20, null=False, editable=False)
    full_name = models.CharField(max_length=40, null=False, blank=False)
    email_address = models.EmailField(max_length=300, null=False, blank=False)
    contact_number = models.CharField(max_length=20, null=False, blank=False)
    town_or_city = models.CharField(max_length=50, null=False, blank=False)
    street_name_1 = models.CharField(max_length=100, null=False, blank=False)
    street_name_2 = models.CharField(max_length=100, null=False, blank=False)
    county = models.CharField(max_length=50, null=False, blank=False)
    postal_code = models.CharField(max_length=15, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    delivery_costs = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(max_digits=8, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(max_digits=8, decimal_places=2, null=False, default=0)
    original_shopping_bag = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')


    def _generate_an_order_number(self):

        return uuid.uuid4().hex.upper()

    def update_total(self):

        self.order_total = self.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum'] or 0
        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_costs = self.order_total * settings.STANDARD_DELIVERY_PERCENTAGE / 100
        else:
            self.delivery_costs = 0
        self.grand_total = self.order_total + self.delivery_costs
        self.save()

    def save(self, *args, **kwargs):

        if not self.order_number:
            self.order_number = self._generate_an_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):

    order = models.ForeignKey(OrderInformation, null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems')
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)
    product_size = models.CharField(max_length=3, null=True, blank=True)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)

    def save(self, *args, **kwargs):

        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Product Number {self.product.product_number} on order {self.order.order_number}'
