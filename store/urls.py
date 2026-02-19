from django.urls import path

from . import views

urlpatterns = [
    path("", views.item_list, name="item-list"),
    path("items/add/", views.item_create, name="item-add"),
    path("items/<int:pk>/edit/", views.item_update, name="item-edit"),
    path("items/<int:pk>/delete/", views.item_delete, name="item-delete"),
    path("categories/add/", views.category_create, name="category-add"),
    path("subcategories/add/", views.subcategory_create, name="subcategory-add"),
    path("api/subcategories/", views.subcategories_by_category, name="subcategory-by-category"),
    path("size-chart/", views.plumbing_size_chart, name="size-chart"),
]
