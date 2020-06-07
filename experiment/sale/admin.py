from django.contrib import admin

from .models import Sale, UnleashedLineItem, UnleashedSalesOrder

# Register your models here.
admin.site.register(Sale)
admin.site.register(UnleashedLineItem)
admin.site.register(UnleashedSalesOrder)
