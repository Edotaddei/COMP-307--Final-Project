from django.db import models
from django.contrib.auth.models import User


def get_upload_path(instance, filename):
    return 'user-' + str(instance.owner.id) + '/' + filename


class Product(models.Model):
    CATEGORY_CHOICES = (
        ('clothing', 'CLOTHING'),
        ('furniture', 'FURNITURE'),
        ('electronics', 'ELECTRONICS'),
        ('other', 'OTHER')
    )
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    count = models.PositiveIntegerField()
    image = models.ImageField(upload_to=get_upload_path, null=True, blank=True)
    category = models.CharField(max_length=50)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name




class OrderProduct(models.Model):
    is_ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.product.name
    #so if there are 2 tshirts this calculates the cost of both tshirts together
    def get_product_count_price(self):

        return self.count* self.product.price


class Order(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    is_ordered = models.BooleanField(default=False)
    products = models.ManyToManyField(OrderProduct)

    def __str__(self):
        return str(self.id)

    def get_total_price(self):
        price = 0
        for p in self.products.all():
            price += p.product.price * p.count
        return price

    def summary(self):
        ret_string = 'Order ID :' + str(self.id)
        ret_string += ', Ordered on: '
        ret_string+= str(self.date.day) + '/' + str(self.date.month) +'/' + str(self.date.year)
        return ret_string

class Address(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    street = models.CharField(max_length=100)
    number = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.street



class TradeProduct(models.Model):
    is_ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name


class TradeRequest(models.Model):
    requester = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver_username = models.CharField(max_length=100)
    is_accepted = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    is_concluded = models.BooleanField(default=False)
    products = models.ManyToManyField(TradeProduct)

    def __str__(self):
        return self.requester.username + 's trade request'
    

