# Generated by Django 4.1.3 on 2023-01-05 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0006_remove_productingredient_qty"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productingredient",
            name="amount",
            field=models.FloatField(),
        ),
    ]