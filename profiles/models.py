from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_full_name = models.CharField(max_length=40, null=True, blank=True)
    default_email_address = models.EmailField(max_length=300, null=True, blank=True)
    default_contact_number = models.CharField(max_length=20, null=True, blank=True)
    default_street_name_1 = models.CharField(max_length=100, null=True, blank=True)
    default_street_name_2 = models.CharField(max_length=100, null=True, blank=True)
    default_town_or_city = models.CharField(max_length=50, null=True, blank=True)
    default_county = models.CharField(max_length=50, null=True, blank=True)
    default_postal_code = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):

    if created:
        UserProfile.objects.create(user=instance)

    instance.userprofile.save()
