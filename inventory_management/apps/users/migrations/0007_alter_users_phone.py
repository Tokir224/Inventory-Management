# Generated by Django 4.1.3 on 2023-01-05 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0006_alter_users_phone"),
    ]

    operations = [
        migrations.AlterField(
            model_name="users",
            name="phone",
            field=models.CharField(blank=True, max_length=15, unique=True),
        ),
    ]
