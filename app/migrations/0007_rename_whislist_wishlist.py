# Generated by Django 5.1.7 on 2025-04-09 06:07

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_whislist'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Whislist',
            new_name='Wishlist',
        ),
    ]
