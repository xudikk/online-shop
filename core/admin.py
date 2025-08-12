from django.contrib import admin
from .models import Category, Product, Cart, Brand
# Register your models here.


class ProductInline(admin.StackedInline):
    model = Product
    extra = 1




@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'deleted']
    inlines = [ProductInline]


admin.site.register(Product)
admin.site.register(Brand)
admin.site.register(Cart)

