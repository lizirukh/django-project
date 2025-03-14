# Generated by Django 5.1.6 on 2025-03-10 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_bookslist_left_in_stock_buybook'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookslist',
            name='left_in_stock',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='buybook',
            name='book_count',
            field=models.PositiveIntegerField(),
        ),
    ]
