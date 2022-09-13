from django.contrib import admin
from django.db import models
from django.db.models import F, Sum
from django.core.validators import MinValueValidator
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
            .filter(availability=True)
            .values_list('product')
        )
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=200,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name='ресторан',
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f'{self.restaurant.name} - {self.product.name}'


class OrderQuerySet(models.QuerySet):

    def order_with_cost(self):
        order_items_with_costs = self.annotate(
            cost=Sum(F('order_items__cost'))
        )\
        .order_by('id')
        return order_items_with_costs


class Order(models.Model):
    PAY_METHODS = (
        ('elec', 'Электронно'),
        ('cash', 'Наличные'),
    )
    STATUSES = (
        ('0', 'Необработанный'),
        ('1', 'Собирается'),
        ('2', 'Доставляется'),
        ('3', 'Выполнен')
    )
    firstname = models.CharField(
        'имя',
        max_length=50
    )
    lastname = models.CharField(
        'фамилия',
        max_length=50
    )
    phonenumber = PhoneNumberField(
        'номер телефона',
        db_index=True,
    )
    address = models.CharField(
        'адрес',
        max_length=150
    )
    pay_method = models.CharField(
        max_length=4,
        choices=PAY_METHODS,
        db_index=True,
        verbose_name='Способ оплаты',
    )
    created_at = models.DateTimeField(
        'создан',
        default=timezone.now,
        db_index=True,
    )
    called_at = models.DateTimeField(
        'позвонили',
        blank=True,
        null=True,
        db_index=True,
    )
    delivered_at = models.DateTimeField(
        'доставлено',
        blank=True,
        null=True,
        db_index=True,
    )
    status = models.CharField(
        max_length=1,
        choices=STATUSES,
        default='0',
        db_index=True,
        verbose_name='Статус',
    )
    comment = models.TextField(
        verbose_name='Комментарий',
        blank=True,
    )
    selected_restaurant = models.ForeignKey(
        Restaurant,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='executable_orders',
        verbose_name='Ресторан, выполняющий заказ',
    )

    objects = OrderQuerySet.as_manager()

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'Заказ №{self.id}'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='items',
        verbose_name='заказ',
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        related_name='order_items',
        verbose_name='продукт',
        on_delete=models.CASCADE,
    )
    quantity = models.IntegerField(
        'количество',
        validators=[MinValueValidator(1)],
    )
    cost = models.DecimalField(
        'стоимость',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )

    class Meta:
        verbose_name = 'состав заказа'
        verbose_name_plural = 'составы заказа'

    def __str__(self):
        return f'{self.product.name} - {self.quantity}'
