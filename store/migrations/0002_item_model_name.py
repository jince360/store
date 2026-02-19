from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="item",
            name="model_name",
            field=models.CharField(blank=True, default="", max_length=180),
        ),
    ]
