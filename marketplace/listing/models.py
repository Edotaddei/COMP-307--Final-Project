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
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    count = models.PositiveIntegerField()
    image = models.ImageField(upload_to=get_upload_path, null=True, blank=True)
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('books:detail', args=[self.id])


