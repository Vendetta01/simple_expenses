# Generated by Django 4.2.3 on 2023-08-06 17:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("transactions", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="transaction",
            name="comment",
            field=models.TextField(null=True),
        ),
    ]
