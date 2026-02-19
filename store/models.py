from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name="subcategories", on_delete=models.CASCADE)
    name = models.CharField(max_length=120)

    class Meta:
        ordering = ["name"]
        unique_together = ("category", "name")

    def __str__(self):
        return f"{self.category.name} - {self.name}"


class Item(models.Model):
    category = models.ForeignKey(Category, related_name="items", on_delete=models.PROTECT)
    subcategory = models.ForeignKey(SubCategory, related_name="items", on_delete=models.PROTECT)
    model_name = models.CharField(max_length=180, blank=True, default="")
    name = models.CharField(max_length=180)
    sku = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        unique_together = ("subcategory", "name")

    def __str__(self):
        return self.name
