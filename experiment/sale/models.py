from django.db import models

# Create your models here.
from catalog.models import Product

class Sale(models.Model):
    created = models.DateTimeField()
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    
    def __str__(self):
        """Creation date of Sale """
        return self.created