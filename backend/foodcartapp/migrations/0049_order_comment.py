# Generated by Django 3.2 on 2022-08-14 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0048_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='comment',
            field=models.TextField(blank=True, max_length=500, verbose_name='Комментарий'),
        ),
    ]