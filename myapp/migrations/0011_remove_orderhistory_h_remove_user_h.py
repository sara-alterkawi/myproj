# Generated by Django 4.2.6 on 2024-01-10 18:45

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0010_alter_user_options_orderhistory_status_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="orderhistory",
            name="H",
        ),
        migrations.RemoveField(
            model_name="user",
            name="H",
        ),
    ]