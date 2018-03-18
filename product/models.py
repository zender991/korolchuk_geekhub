from django.db import models
from django.contrib.postgres.fields import JSONField


class Category(models.Model):
    title = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class Subcategory(models.Model):
    category = models.ManyToManyField(Category, related_name='subcategories')
    title = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Subcategories'

    def __str__(self):
        return self.title


class Product(models.Model):
    subcategory = models.ManyToManyField(Subcategory)

    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.FloatField(default=0.0)
    quantity = models.IntegerField()
    sku = models.CharField(max_length=50, unique=True, default='111111')
    image = models.FileField(null=True, blank=True)
    meta_keywords = models.CharField(max_length=200, default='')
    meta_description = models.CharField(max_length=200, default='')
    on_the_main = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Order(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    order_details = JSONField(default={})
    subtotal = models.FloatField()

    def __str__(self):
        return self.email


class Currency(models.Model):
    title = models.CharField(max_length=50)
    value = models.FloatField()