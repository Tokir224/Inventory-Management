# Generated by Django 4.1.3 on 2022-12-09 04:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0002_productingredient"),
    ]

    operations = [
        migrations.AlterModelTable(
            name="productingredient",
            table="product_ingredient",
        ),
    ]
