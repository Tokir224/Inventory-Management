# Generated by Django 4.1.3 on 2022-12-09 06:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0004_productingredient_qty_alter_productingredient_amount"),
    ]

    operations = [
        migrations.RenameField(
            model_name="productingredient",
            old_name="Qty",
            new_name="qty",
        ),
    ]
