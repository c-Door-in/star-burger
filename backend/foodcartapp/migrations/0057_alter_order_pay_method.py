# Generated by Django 3.2 on 2022-09-13 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0056_alter_order_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='pay_method',
            field=models.CharField(choices=[('elec', 'Электронно'), ('cash', 'Наличные')], db_index=True, max_length=4, verbose_name='Способ оплаты'),
        ),
    ]
