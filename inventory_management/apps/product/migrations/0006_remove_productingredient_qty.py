# Generated by Django 4.1.3 on 2023-01-05 08:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0005_rename_qty_productingredient_qty"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="productingredient",
            name="qty",
        ),
    ]