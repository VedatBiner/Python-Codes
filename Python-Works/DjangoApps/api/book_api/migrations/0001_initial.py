# Generated by Django 4.1.3 on 2023-02-14 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ttile', models.CharField(max_length=100)),
                ('page_number', models.IntegerField()),
                ('publish_date', models.DateField()),
                ('stock', models.IntegerField()),
            ],
        ),
    ]
