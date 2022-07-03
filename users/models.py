from django.db import models
from django.conf import settings
from services.models import Service
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.

SERVICE_CHOICES = (
    ('SOFT SERVICE', 'SOFT SERVICE'),
    ('HARD SERVICE', 'HARD SERVICE'),
)


class RenderedServices(models.Model):
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="rendered_to", on_delete=models.CASCADE, blank=True, null=True)
    ordered_service = models.ForeignKey(Service, on_delete=models.CASCADE)
    negotiate = models.BooleanField(default=False, null=True)
    service_ordered_date = models.DateTimeField(auto_now_add=True)
    service_price = models.IntegerField()
    completed_by_user = models.BooleanField(default=False, blank=True, null=True)
    completed_by_provider = models.BooleanField(default=False, blank=True, null=True)
    user_paid = models.BooleanField(default=False, blank=True, null=True)
    provider_paid = models.BooleanField(default=False, blank=True, null=True)
    ref_code = models.CharField(max_length=20)

class OrderCompletedServices(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="rendered_by", on_delete=models.CASCADE, blank=True, null=True)
    ordered_service = models.ForeignKey(Service, on_delete=models.CASCADE)
    negotiate = models.BooleanField(default=False, null=True)
    service_ordered_date = models.DateTimeField(auto_now_add=True)
    service_price = models.IntegerField()
    completed_by_user = models.BooleanField(default=False, blank=True, null=True)
    completed_by_provider = models.BooleanField(default=False, blank=True, null=True)
    user_paid = models.BooleanField(default=False, blank=True, null=True)
    provider_paid = models.BooleanField(default=False, blank=True, null=True)
    ref_code = models.CharField(max_length=20)

# details of all users
class UserProfile(models.Model):
    person = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="profile", on_delete=models.CASCADE,  blank=True, null=True)
    profile_pic = models.ImageField(blank=True, upload_to="Profile/")
    state = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    is_a_provider = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.person

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
    proof_of_address = models.ImageField(blank=False, upload_to="AddressProof/")
    identity_proof = models.CharField(choices=Identity_CHOICES, blank=False, max_length=100)
    identity_proof_pic = models.ImageField(blank=False, upload_to="IdentityProof/")
    identity_proof_no = models.IntegerField(blank=False)
    bank_name = models.CharField(max_length=300)
    bank_acc_number = models.IntegerField()

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


