from django.db import models
from django.contrib.auth.models import User


def get_upload_path(instance, filename):
    return 'user-' + str(instance.owner.id) + '/' + filename


class Product(models.Model):
    CATEGORY_CHOICES = (
        ('clothing', 'CLOTHING'),
        ('furniture', 'FURNITURE'),
        ('electronics', 'ELECTRONICS')
    )
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    count = models.PositiveIntegerField()
    image = models.ImageField(upload_to=get_upload_path, null=True, blank=True)
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Address(models.Model):
    street = models.CharField(max_length=100)
    number = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)
    country = models.CharField(max_length=100)


class OrderProduct(models.Model):
    is_ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.product.name


class Order(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField()
    is_ordered = models.BooleanField(default=False)
    products = models.ManyToManyField(OrderProduct)

    def __str__(self):
        return self.owner.username

    def get_total_price(self):
        price = 0
        for p in self.products.all():
            price += p.product.price * p.count
        return price
