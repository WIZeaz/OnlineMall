# Generated by Django 2.1.7 on 2019-07-10 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_order_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.IntegerField(default=1, verbose_name='status'),
            preserve_default=False,
        ),
    ]
