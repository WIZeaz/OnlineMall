# Generated by Django 2.1.7 on 2019-07-10 17:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20190711_0111'),
    ]

    operations = [
        migrations.CreateModel(
            name='order_item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(verbose_name='amount')),
                ('toOrder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='main.order')),
                ('toSKU', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main.SKU')),
            ],
        ),
    ]
