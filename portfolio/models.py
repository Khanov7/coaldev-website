from django.db import models
from datetime import date
from django.utils.timezone import now
# Create your models here.


class Category(models.Model):

    category_name = models.TextField(max_length=30)
    Category_details = models.TextField(max_length=2000)
    category_image = models.FileField()
    number_of_orders = models.IntegerField(default=0)

    def __str__(self):
        return self.category_name+'------'+str(self.number_of_orders)


class Order(models.Model):

    order_name = models.TextField(max_length=200)
    order_abstract = models.TextField(max_length=2000)
    order_details = models.TextField(max_length=5000)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    order_date = models.DateField(null=True)
    order_image = models.FileField(default='')
    def __str__(self):
        return self.order_name+'-------'+self.order_abstract

