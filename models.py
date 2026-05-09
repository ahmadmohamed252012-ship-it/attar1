from django.db import models

class Product(models.Model):

    name = models.CharField(max_length=200)
    price = models.IntegerField()

    image = models.ImageField(upload_to='products')

    image2 = models.ImageField(upload_to='products', blank=True, null=True)
    image3 = models.ImageField(upload_to='products', blank=True, null=True)
    image4 = models.ImageField(upload_to='products', blank=True, null=True)
    image5 = models.ImageField(upload_to='products', blank=True, null=True)

    description = models.TextField(blank=True)

    brand = models.CharField(max_length=100, blank=True)
    ram = models.CharField(max_length=50, blank=True)
    storage = models.CharField(max_length=50, blank=True)
    battery = models.CharField(max_length=100, blank=True)
    camera = models.CharField(max_length=100, blank=True)
    condition = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def total(self):
        return self.product.price * self.quantity