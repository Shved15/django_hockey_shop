import stripe
from django.conf import settings
from django.db import models

from users.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY


# A model to represent the product category.
class ProductCategory(models.Model):
    name = models.CharField(max_length=128, unique=True, help_text='Limit: 128 characters!')
    description = models.TextField(max_length=1024, null=True, blank=True, help_text='Limit: 1024 characters!')

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


# A model representing a product in the store.
class Product(models.Model):
    name = models.CharField(max_length=128, help_text='Limit: 128 characters')
    description = models.TextField(max_length=2048, help_text='Limit: 2048 characters!')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products_images')
    stripe_product_price_id = models.CharField(max_length=128, null=True, blank=True)
    category = models.ForeignKey(to=ProductCategory, on_delete=models.PROTECT)

    # responsible for additional lines
    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'

    # Returns a string representation of the product.
    def __str__(self) -> str:
        return f'Product: {self.name} || Category: {self.category.name}'

    # method of storing objects in the DB
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None) -> None:
        """Overrides the save method of the model."""
        # if stripe-id is not filled then create it
        if not self.stripe_product_price_id:
            stripe_product_price = self.create_stripe_product_price()
            self.stripe_product_price_id = stripe_product_price['id']
        super(Product, self).save(force_insert=False, force_update=False, using=None,
                                  update_fields=None)

    def create_stripe_product_price(self) -> dict:
        """ Creates a product and its price in Stripe."""
        stripe_product = stripe.Product.create(name=self.name)
        stripe_product_price = stripe.Price.create(
            product=stripe_product['id'],
            unit_amount=round(self.price * 100),
            currency="usd"
        )
        return stripe_product_price


# QuerySet model of Bag
class BagQuerySet(models.QuerySet):
    # Calculate total price of all products in bag
    def total_sum(self) -> float:
        return sum(bag.sum() for bag in self)

    # Calculate total quantity of all products in bag
    def total_quantity(self) -> int:
        return sum(bag.quantity for bag in self)

    # Logic for creating line_items in order.views.OrderCreateView.post
    def stripe_products(self) -> list:
        line_items = []
        for bag in self:
            item = {
                'price': bag.product.stripe_product_price_id,
                'quantity': bag.quantity,
            }
            line_items.append(item)
        return line_items


# bag model
class Bag(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    # QuerySet object as manager
    objects = BagQuerySet().as_manager()

    def __str__(self) -> str:
        return f'Bag for {self.user.username} ||| Product for {self.product.name}'

    def sum(self) -> float:
        return self.product.price * self.quantity

    def de_json(self) -> dict:
        """Return a dictionary representation of the Bag object that can be serialized to JSON."""
        bag_item = {
            'product_name': self.product.name,
            'quantity': self.quantity,
            'price': float(self.product.price),
            'sum': float(self.sum()),
        }
        return bag_item

    @classmethod
    def create_or_update(cls, product_id, user) -> tuple:
        """Create a new Bag object or update the quantity of an existing Bag object."""
        bags = Bag.objects.filter(user=user, product_id=product_id)

        if not bags.exists():
            obj = Bag.objects.create(user=user, product_id=product_id, quantity=1)
            is_created = True
            return obj, is_created
        else:
            bag = bags.first()
            bag.quantity += 1
            bag.save()
            is_crated = False
            return bag, is_crated


class Favorites(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s favorites products."
