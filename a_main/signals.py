from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from .models import Customer
from django.shortcuts import get_object_or_404

@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    user = instance
    if created:
        Customer.objects.create(
            user = user,
            email = user.email
        )
    else:
        profile  = get_object_or_404(Customer, user=user)
        profile.email = user.email
        profile.save()