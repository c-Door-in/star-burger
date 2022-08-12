# Generated by Django 3.2 on 2022-06-16 10:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0042_alter_order_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.CharField(max_length=150, verbose_name='адрес'),
        ),
        migrations.AlterField(
            model_name='order',
            name='lastname',
            field=models.CharField(max_length=50, verbose_name='фамилия'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='foodcartapp.order', verbose_name='заказ'),
        ),
    ]