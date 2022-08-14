# Generated by Django 3.2 on 2022-08-14 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0046_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('0', 'Необработанный'), ('1', 'Собирается'), ('2', 'Доставляется'), ('3', 'Выполнен')], db_index=True, default='0', max_length=1),
        ),
    ]