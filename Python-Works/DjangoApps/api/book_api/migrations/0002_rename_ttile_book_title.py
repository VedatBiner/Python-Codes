# Generated by Django 4.1.3 on 2023-02-15 05:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book_api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='ttile',
            new_name='title',
        ),
    ]
