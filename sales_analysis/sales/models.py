from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=255, null=True, blank=True)
    product_brand = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Address(models.Model):
    postal_code = models.CharField(max_length=10)
    city = models.CharField(max_length= 255)
    street = models.CharField(max_length=255)
    building_number = models.DecimalField(max_digits=10, decimal_places=0)
    local_number = models.DecimalField(max_digits=10, decimal_places=0)

    def __str__(self):
        return f"City: {self.city}, Street: {self.street} {self.building_number}/{self.local_number}, postal-code: {self.postal_code}"

class Customer(models.Model):
    name = models.CharField(max_length=255)
    phone = models.DecimalField(max_digits=14, decimal_places=0)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null= True, blank= True)
    e_mail = models.EmailField(max_length=255)

class OrderDetail(models.Model):
    products = models.ManyToManyField(Product, through='OrderProduct')
    delivery_address = models.CharField(max_length=255)
    order_notes = models.TextField(null=True, blank=True)

    @property
    def final_price(self):
        total_price = sum(order_product.product.price * order_product.quantity for order_product in self.order_products.all())
        return total_price

class OrderProduct(models.Model):
    order_detail = models.ForeignKey(OrderDetail, on_delete=models.CASCADE, related_name='order_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = 'P', 'Pending'
        PROCESSING = 'PR', 'Processing'
        SHIPPED = 'S', 'Shipped'
        DELIVERED = 'D', 'Delivered'
        CANCELED = 'C', 'Canceled'

    order_status = models.CharField(max_length=2, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    orderdetail = models.ForeignKey(OrderDetail, on_delete=models.PROTECT)
    ordered_date = models.DateTimeField(auto_now=True)
    delivery_date = models.DateTimeField(null=True, default=None)

@receiver(pre_delete, sender=Order)
def protect_customer_on_delete(sender, instance, **kwargs):
    if instance.order_status != Order.OrderStatus.CANCELED:
        instance.customer.on_delete = models.PROTECT
        instance.customer.save()
    else:
        instance.customer.on_delete = models.CASCADE
        instance.customer.save()