# Generated by Django 2.1.7 on 2019-07-10 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='address',
            field=models.TextField(verbose_name='address'),
        ),
    ]
