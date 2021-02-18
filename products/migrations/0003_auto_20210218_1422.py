# Generated by Django 3.1.6 on 2021-02-18 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20210212_1539'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_sizes',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_number',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
    ]