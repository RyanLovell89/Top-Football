# Generated by Django 3.1.6 on 2021-02-26 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0004_orderinformation_user_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderinformation',
            name='order_number',
            field=models.CharField(editable=False, max_length=32),
        ),
    ]