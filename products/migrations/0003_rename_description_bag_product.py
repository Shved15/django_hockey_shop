# Generated by Django 3.2.13 on 2023-03-06 13:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_bag'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bag',
            old_name='description',
            new_name='product',
        ),
    ]
