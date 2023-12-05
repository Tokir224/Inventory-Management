# Generated by Django 4.1.3 on 2023-01-05 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("raw_material", "0003_alter_productrawmaterial_table"),
    ]

    operations = [
        migrations.AddField(
            model_name="productrawmaterial",
            name="product_type",
            field=models.IntegerField(
                choices=[(1, "Solid"), (2, "Liquid"), (3, "Pieces")], default=1
            ),
            preserve_default=False,
        ),
    ]