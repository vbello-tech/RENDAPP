from django.db import models
from django.conf import settings
from Service.models import Service
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import RegexValidator
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

SERVICE_CHOICES = (
    ('SOFT SERVICE', 'SOFT SERVICE'),
    ('HARD SERVICE', 'HARD SERVICE'),
)


class RenderedServices(models.Model):
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="redendered_to", blank=True, null=True, on_delete=models.CASCADE)
    ordered_service = models.ForeignKey(Service, on_delete=models.CASCADE)
    service_ordered_date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    ref_code = models.CharField(max_length=20)

class CompletedOrderedServices(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="redendered_by", blank=True, null=True, on_delete=models.CASCADE)
    ordered_service = models.ForeignKey(Service, on_delete=models.CASCADE)
    service_ordered_date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    ref_code = models.CharField(max_length=20)

# details of all users
class UserProfile(models.Model):
    person = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="profile", on_delete=models.CASCADE,  blank=True, null=True)
    profile_pic = models.ImageField(blank=True, upload_to="Profile/")
    phone_number = PhoneNumberField(blank=True, null=True)
    state = models.CharField(max_length=30, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    is_a_provider = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.person.username

Identity_CHOICES = (
    ('NIN', 'NIN'),
    ('DRIVERS LICENSE', 'DRIVERS LICENSE'),
)

# details if user is a provider
class ServiceOwnerDetails(models.Model):
    person = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    state = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    use_profile_address = models.BooleanField(default=False, blank=True, null=True)
    proof_of_address = models.ImageField(blank=False, upload_to="AddressProof/")
    identity_proof = models.CharField(choices=Identity_CHOICES, blank=False, max_length=100)
    identity_proof_pic = models.ImageField(blank=False, upload_to="IdentityProof/")
    identity_proof_no = models.IntegerField(blank=False)

    def __str__(self):
        return self.person

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def user_profile(sender, instance, created, *args, **kwargs):
    if created:
        UserProfile.objects.create(person=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, created, *args, **kwargs):
    try:
        instance.profile.save()
    except ObjectDoesNotExist:
        UserProfile.objects.create(person=instance)


