# Generated by Django 3.2.6 on 2021-08-30 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Productmanagement', '0005_alter_cart_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='product',
            field=models.ManyToManyField(blank=True, to='Productmanagement.Product'),
        ),
    ]