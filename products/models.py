from django.db import models

from users.models import User


# create categories of product model
class ProductCategory(models.Model):
    name = models.CharField(max_length=128, unique=True, help_text='Limit: 128 characters!')
    description = models.TextField(max_length=1024, null=True, blank=True, help_text='Limit: 1024 characters!')

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


# create product model
class Product(models.Model):
    name = models.CharField(max_length=128, help_text='Limit: 128 characters')
    description = models.TextField(max_length=2048, help_text='Limit: 2048 characters!')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products_images')
    category = models.ForeignKey(to=ProductCategory, on_delete=models.PROTECT)

    # responsible for additional lines
    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'

    # good output in the admin panel
    def __str__(self):
        return f'Product: {self.name} || Category: {self.category.name}'


# create QuerySet model of Bag
class BagQuerySet(models.QuerySet):
    # total price of all products in bag
    def total_sum(self):
        return sum(bag.sum() for bag in self)

    # total quantity of all products in bag
    def total_quantity(self):
        return sum(bag.quantity for bag in self)


# create bag model
class Bag(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    # create QuerySet object as manager
    objects = BagQuerySet().as_manager()

    def __str__(self):
        return f'Bag for {self.user.username} ||| Product for {self.product.name}'

    def sum(self):
        return self.product.price * self.quantity

