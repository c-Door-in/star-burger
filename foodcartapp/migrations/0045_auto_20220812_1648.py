# Generated by Django 3.2 on 2022-08-12 13:48

from django.db import migrations


def define_old_orders_cost(app, schema_editor):
    OrderItem = app.get_model('foodcartapp', 'OrderItem')
    empty_cost_items = OrderItem.objects.filter(cost=0.00)
    for item in empty_cost_items:
        item.cost = item.product.price*item.quantity
        item.save()


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0044_orderitem_cost'),
    ]

    operations = [
        migrations.RunPython(define_old_orders_cost)
    ]