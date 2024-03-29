from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Review(models.Model):
    RATING_OPTIONS = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5')
    )
    rating = models.CharField(max_length=10, choices = RATING_OPTIONS, default='4')
    comment = models.TextField( blank=True, null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.rating


class Product(models.Model) :
    name = models.CharField(max_length=200)
    price = models.IntegerField(blank=True)
    category = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    image = models.ImageField(upload_to='products/images/', blank=True, null=True)
    file = models.FileField(upload_to='products/files/', blank=True, null=True)

    reviews = models.ManyToManyField(Review)

    def __str__(self):
        return self.name

class Cart(models.Model) :
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product, blank=True)

    created_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.user.username

class Order(models.Model) :
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)

    created_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Delivering', 'Delivering'),
        ('Completed', 'Completed')
    )

    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default='Pending')

    PAYMENT_CHOICES = (
        ('Bkash', 'Bkash'),
        ('Rocket', 'Rocket'),
        ('Cash on Delivery', 'Cash on Delivery')
    )

    payment_options = models.CharField(max_length=50, choices=PAYMENT_CHOICES, default='Cash on Delivery')
    is_paid = models.BooleanField(default=False)

    transaction_id = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self) :
        return self.user.username + "_" + self.product.name + "_" + self.status

class FAQ(models.Model):
    STATUS = (
        ("True", "True"),
        ("False", "False"),
    )

    ordernumber = models.IntegerField()
    question = models.CharField(max_length=300)
    answer = models.TextField()
    status = models.CharField(choices=STATUS, max_length=100, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question