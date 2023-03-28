from django.db import models

from products.models import Bag
from users.models import User


class Order(models.Model):
    CREATED = 0
    PAID = 1
    ON_WAY = 2
    DELIVERED = 3
    STATES = (
        (CREATED, 'Created'),
        (PAID, 'Paid'),
        (ON_WAY, 'On way'),
        (DELIVERED, 'Delivered'),
    )

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=128)
    address = models.CharField(max_length=256)
    bag_history = models.JSONField(default=dict)
    created = models.DateTimeField(auto_now_add=True)
    state = models.SmallIntegerField(default=CREATED, choices=STATES)
    creator = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Order №{self.id}. {self.first_name} {self.last_name}'

    # get json data about the order after payment in bag_history
    # with deleting items from the bag
    def update_after_payment(self):
        bags = Bag.objects.filter(user=self.creator)
        self.state = self.PAID
        self.bag_history = {
            'purchased_items': [bag.de_json() for bag in bags],
            'total_sum': float(bags.total_sum()),
        }
        bags.delete()
        self.save()
