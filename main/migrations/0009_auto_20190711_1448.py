# Generated by Django 2.1.7 on 2019-07-11 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_order_snap_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='confirm_time',
            field=models.DateTimeField(null=True, verbose_name='confirm_time'),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_time',
            field=models.DateTimeField(null=True, verbose_name='payment_time'),
        ),
    ]
