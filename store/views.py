from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CategoryForm, ItemForm, SubCategoryForm
from .models import Category, Item, SubCategory


@login_required
def item_list(request):
    category_id = request.GET.get("category")
    subcategory_id = request.GET.get("subcategory")
    query = request.GET.get("q", "").strip()

    items = Item.objects.select_related("category", "subcategory")
    subcategories = SubCategory.objects.select_related("category")

    if category_id:
        items = items.filter(category_id=category_id)
        subcategories = subcategories.filter(category_id=category_id)
    if subcategory_id:
        items = items.filter(subcategory_id=subcategory_id)
    if query:
        items = items.filter(
            Q(name__icontains=query)
            | Q(model_name__icontains=query)
            | Q(sku__icontains=query)
            | Q(description__icontains=query)
            | Q(category__name__icontains=query)
            | Q(subcategory__name__icontains=query)
        )

    context = {
        "items": items,
        "categories": Category.objects.all(),
        "subcategories": subcategories,
        "selected_category": category_id or "",
        "selected_subcategory": subcategory_id or "",
        "query": query,
    }
    return render(request, "store/item_list.html", context)


@login_required
def item_create(request):
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("item-list")
    else:
        form = ItemForm()
    return render(request, "store/item_form.html", {"form": form, "title": "Add Item"})


@login_required
def item_update(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == "POST":
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("item-list")
    else:
        form = ItemForm(instance=item)
    return render(request, "store/item_form.html", {"form": form, "title": "Edit Item"})


@login_required
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == "POST":
        item.delete()
        return redirect("item-list")
    return render(request, "store/item_confirm_delete.html", {"item": item})


@login_required
def category_create(request):
    next_url = request.GET.get("next") or request.POST.get("next") or "item-list"
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(next_url)
    else:
        form = CategoryForm()
    return render(request, "store/category_form.html", {"form": form, "next_url": next_url})


@login_required
def subcategory_create(request):
    next_url = request.GET.get("next") or request.POST.get("next") or "item-list"
    if request.method == "POST":
        form = SubCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(next_url)
    else:
        form = SubCategoryForm()
    return render(request, "store/subcategory_form.html", {"form": form, "next_url": next_url})


@login_required
def subcategories_by_category(request):
    category_id = request.GET.get("category_id")
    subcategories = SubCategory.objects.none()
    if category_id:
        subcategories = SubCategory.objects.filter(category_id=category_id).order_by("name")
    data = [{"id": subcategory.id, "name": subcategory.name} for subcategory in subcategories]
    return JsonResponse({"subcategories": data})


@login_required
def plumbing_size_chart(request):
    size_chart = [
        ("1/8", "DN 6"),
        ("1/4", "DN 8"),
        ("3/8", "DN 10"),
        ("1/2", "DN 15"),
        ("3/4", "DN 20"),
        ("1", "DN 25"),
        ("1 1/4", "DN 32"),
        ("1 1/2", "DN 40"),
        ("2", "DN 50"),
        ("2 1/2", "DN 65"),
        ("3", "DN 80"),
        ("4", "DN 100"),
        ("5", "DN 125"),
        ("6", "DN 150"),
    ]
    return render(request, "store/size_chart.html", {"size_chart": size_chart})
