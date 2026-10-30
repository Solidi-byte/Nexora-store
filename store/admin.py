from django.contrib import admin
from .models import Product, Category, Order

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Remove 'created_at' from here if it's causing the error
    list_display = ('name', 'category', 'price') 

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'product', 'color', 'size', 'total_amount', 'created_at')