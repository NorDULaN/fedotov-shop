from django.db import models
from products.models import Product
from django.db.models.signals import post_save
#from django.contrib.auth.models import User


class OrderStatus(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = "Статус заказа"
        verbose_name_plural = "Статусы заказа"


class Order(models.Model):
    #user = models.ForeignKey(User, blank=True, null=True, default=None, on_delete=models.CASCADE)
    customer_name = models.CharField(verbose_name="ФИО",max_length=80, blank=False, null=True, default=None)
    customer_email = models.EmailField(verbose_name="EMAIL",blank=False, null=True, default=None)
    customer_phone = models.CharField(verbose_name="Номер телефона",max_length=48, blank=False, null=True, default=None)
    customer_region = models.CharField(verbose_name="Регион/Область",max_length=60, blank=False, null=True, default=None)
    customer_city = models.CharField(verbose_name="Город/Дом",max_length=48, blank=False, null=True, default=None)
    customer_index = models.IntegerField(verbose_name="Почтовый индекс",blank=False, null=True, default=None)
    customer_comment = models.TextField(verbose_name="Комментарий к заказу",blank=True, null=True, default=None)
    status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "Заказ id:%s - %s" % (self.id, self.status.name)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class ProductInOrder(models.Model):
    order = models.ForeignKey(Order, blank=True, null=True, default=None, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, blank=True, null=True, default=None, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % self.product.name

    class Meta:
        verbose_name = "Товар в заказе"
        verbose_name_plural = "Товары в заказе"

    def save(self, *args, **kwargs):
        price_per_item = 0
        if self.product.discount > 0:
            ret_price = self.product.price - (self.product.price / 100 * self.product.discount)
            price_per_item = ret_price
        else:
            price_per_item = self.product.price
        self.price_per_item = price_per_item
        self.total_price = int(self.count) * price_per_item
        super(ProductInOrder, self).save(*args, **kwargs)


def product_in_order_post_save(sender, instance, created, **kwargs):
    order = instance.order
    products_in_order = ProductInOrder.objects.filter(order=order, is_active=True)
    order_total_price = 0
    for item in products_in_order:
        order_total_price += item.total_price
    instance.order.total_price = order_total_price
    instance.order.save(force_update=True) # Обновление записи


post_save.connect(product_in_order_post_save, sender=ProductInOrder)


class ProductInCart(models.Model):
    session_key = models.CharField(max_length=128, blank=True, null=True, default=None,)
    #order = models.ForeignKey(Order, blank=True, null=True, default=None, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, blank=True, null=True, default=None, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % self.product.name

    class Meta:
        verbose_name = "Товар в корзине"
        verbose_name_plural = "Товары в корзине"

    def save(self, *args, **kwargs):
        price_per_item = 0
        if self.product.discount > 0:
            ret_price = self.product.price - (self.product.price / 100 * self.product.discount)
            price_per_item = ret_price
        else:
            price_per_item = self.product.price
        #price_per_item = self.product.price
        self.price_per_item = price_per_item
        self.total_price = int(self.count) * price_per_item
        super(ProductInCart, self).save(*args, **kwargs)
