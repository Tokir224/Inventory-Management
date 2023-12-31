# Generated by Django 4.1.3 on 2022-12-02 11:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("raw_material", "0001_initial"),
        ("product", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProductIngredient",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("amount", models.FloatField()),
                (
                    "type",
                    models.IntegerField(
                        choices=[
                            (1, "KG"),
                            (2, "G"),
                            (3, "MG"),
                            (4, "L"),
                            (5, "ML"),
                            (6, "Pieces"),
                        ]
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="product.product",
                    ),
                ),
                (
                    "raw_material",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="raw_material.productrawmaterial",
                    ),
                ),
            ],
        ),
    ]
