# Generated by Django 4.1.3 on 2022-12-14 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_rename_name_users_first_name_users_last_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="users",
            name="phone",
            field=models.CharField(blank=True, max_length=15, unique=True),
        ),
    ]