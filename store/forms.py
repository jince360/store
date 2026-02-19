from django import forms

from .models import Category, Item, SubCategory


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["category", "subcategory", "name", "model_name", "sku", "description", "price", "stock_quantity"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        subcategory_qs = SubCategory.objects.select_related("category")
        category_id = None

        if self.is_bound:
            category_id = self.data.get("category")
        elif self.instance and self.instance.pk:
            category_id = self.instance.category_id

        if category_id:
            self.fields["subcategory"].queryset = subcategory_qs.filter(category_id=category_id)
        else:
            self.fields["subcategory"].queryset = subcategory_qs.none()

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get("category")
        subcategory = cleaned_data.get("subcategory")
        if category and subcategory and subcategory.category_id != category.id:
            raise forms.ValidationError("Sub category must belong to the selected category.")
        return cleaned_data


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]


class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ["category", "name"]
