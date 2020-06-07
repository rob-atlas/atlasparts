import datetime
from django.db import models

# Create your models here.
from catalog.models import Product

class Sale(models.Model):
    created = models.DateTimeField()
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    def __str__(self):
        """Creation date of Sale """
        return self.created


"""
All sales orders come from Unleashed Inventory Management System
https://au.unleashedsoftware.com

Get read-only data about orders.
Interpret the content so that it makes sense for the manufacturing
department to build the product.

With that in mind the information from Unleashed is via an API and
returns it in json.
So I have re-created a Sales class with only the info I need
I was trying to get the json data straight in to a python class(es)
but it is getting to cumbersome, so reverting back to everything 
being strings
"""
class UnleashedLineItem(models.Model):
    code = models.CharField(max_length=30)
    description = models.CharField(max_length=100, null=True)
    qty = models.CharField(max_length=4, null=True)

    class Meta:
        ordering = ['code']

    def __str__(self):
        return self.code


class UnleashedSalesOrder(models.Model):
    order = models.CharField(max_length=12) # 'SO-00001173'
    venue = models.CharField(max_length=80, null=True) # "Sunbury Bowling Club"
    address = models.CharField(max_length=80, null=True) # "49 Riddell Road"
    town = models.CharField(max_length=25, null=True) # "Sunbury"
    state = models.CharField(max_length=25, null=True) # "VIC"
    postcode = models.CharField(max_length=10, null=True) # "3429"
    comment = models.CharField(max_length=255, null=True) # "Tito kit for serial 330123"
    # order_date = models.DateTimeField(default=datetime.date.today) # "Order date"
    order_date = models.CharField(max_length=20, null=True)
    # install_date = models.DateTimeField(default=datetime.date.today) # "installation date"
    install_date = models.CharField(max_length=20, null=True)
    jurisdiction = models.CharField(max_length=12, null=True) # "VIC H&C"
    line_item = models.ManyToManyField(UnleashedLineItem) # "EGMA3VIC005 26-275"



