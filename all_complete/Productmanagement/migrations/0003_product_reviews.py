# Generated by Django 3.0.9 on 2020-10-05 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Productmanagement', '0002_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='reviews',
            field=models.ManyToManyField(to='Productmanagement.Review'),
        ),
    ]
