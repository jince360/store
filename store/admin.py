from django.contrib import admin

from .models import Category, Item, SubCategory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "category"]
    list_filter = ["category"]
    search_fields = ["name", "category__name"]


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ["name", "model_name", "category", "subcategory", "price", "stock_quantity"]
    list_filter = ["category", "subcategory"]
    search_fields = ["name", "model_name", "sku", "description"]
