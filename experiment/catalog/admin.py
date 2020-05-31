from django.contrib import admin

from .models import Category, Product, GameName, Jurisdiction

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(GameName)
admin.site.register(Jurisdiction)
