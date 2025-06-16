from django.contrib import admin
from .models import Category, Product, Cart, Brand
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'deleted']


admin.site.register(Product)
admin.site.register(Brand)
admin.site.register(Cart)

