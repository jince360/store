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

        # Ensure consistent modern spacing on all generated fields.
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs["class"] = (
                    "w-full rounded-xl border border-slate-300 bg-white/90 px-3 py-2.5 pr-10 text-sm "
                    "focus:outline-none focus:ring-2 focus:ring-cyan-400/70 focus:border-cyan-400"
                )
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs["class"] = (
                    "w-full rounded-xl border border-slate-300 bg-white/90 px-3 py-2.5 text-sm "
                    "focus:outline-none focus:ring-2 focus:ring-cyan-400/70 focus:border-cyan-400"
                )
            else:
                field.widget.attrs["class"] = (
                    "w-full rounded-xl border border-slate-300 bg-white/90 px-3 py-2.5 text-sm "
                    "focus:outline-none focus:ring-2 focus:ring-cyan-400/70 focus:border-cyan-400"
                )

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs["class"] = (
            "w-full rounded-xl border border-slate-300 bg-white/90 px-3 py-2.5 text-sm "
            "focus:outline-none focus:ring-2 focus:ring-cyan-400/70 focus:border-cyan-400"
        )


class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ["category", "name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].widget.attrs["class"] = (
            "w-full rounded-xl border border-slate-300 bg-white/90 px-3 py-2.5 pr-10 text-sm "
            "focus:outline-none focus:ring-2 focus:ring-cyan-400/70 focus:border-cyan-400"
        )
        self.fields["name"].widget.attrs["class"] = (
            "w-full rounded-xl border border-slate-300 bg-white/90 px-3 py-2.5 text-sm "
            "focus:outline-none focus:ring-2 focus:ring-cyan-400/70 focus:border-cyan-400"
        )
