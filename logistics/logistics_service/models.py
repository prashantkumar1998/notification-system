from django.db import models

# Create your models here.
class Tracking(models.Model):
    class Status(models.TextChoices):
        ORDERED = 'ordered'                     
        DISPATCHED = 'dispatched'
        SHIPED = 'shiped'
        OUT_FOR_DELIVERY = 'out_for_delivery'
        DELIVERED = 'delivered'
        PICKED_UP = 'picked_up'
        RETURN_TO_SELLER = 'return_to_seller'
        UNDELIVERED = 'undelivered'
        
    tracking_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.TextField()
    status = models.TextField(choices=Status.choices, default=Status.ORDERED)
    email = models.EmailField(max_length=254, default='')

    def __str__(self):
        return f"Order ID: {self.tracking_id}, Name: {self.name}"
