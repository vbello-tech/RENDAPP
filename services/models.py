from django.db import models
from django.conf import settings
from django.utils import timezone
from django.shortcuts import reverse
# Create your models here.

SERVICE_CHOICES = (
    ('SOFT SERVICE', 'SOFT SERVICE'),
    ('HARD SERVICE', 'HARD SERVICE'),
)

CATEGORY_CHOICES = (
    ('DRY CLEANING', 'DRY CLEANING'),
    ('SALON', 'SALON'),
    ('CARPENTARY AND WOOD WORK', 'CARPENTARY AND WOOD WORK')
)

class Category(models.Model):
    category = models.CharField(max_length=200)
    name = models.CharField(max_length=20, blank=True, null=True)
    category_image = models.ImageField(blank=True, upload_to="Cat Image/")

    def __str_(self):
        return self.category
"""
cat = Category.objects.all().values_list('category', 'category')
CATEGORY_CHOICES = []
for choice in cat:
    CATEGORY_CHOICES.append(choice)
"""
class Service(models.Model):
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    image = models.ImageField(blank=True, upload_to="Service/")
    category = models.CharField(max_length=200, blank =True, null=True, choices=CATEGORY_CHOICES)
    type = models.CharField(choices=SERVICE_CHOICES, default="New", max_length=100)
    active = models.BooleanField(default=False, blank=True)
    service_completed = models.IntegerField(default=0, blank=True, null=True)
    price = models.IntegerField()
    negotiate = models.BooleanField(default=False, null=True)
    max_negotiation_price = models.IntegerField(blank=True, null=True)
    min_negotiation_price = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    banned = models.BooleanField(default=False, blank=True, null=True)
    banned_date = models.DateTimeField(blank=True, null=True)
    service_state = models.CharField(max_length=15, blank=True, null=True)
    service_city = models.CharField(max_length=30, blank=True, null=True)
    service_address = models.CharField(max_length=100, blank=True, null=True)
    service_url = models.URLField(blank=True)

    def get_category(self):
        return reverse("service:category", kwargs={
            'category':self.category,
        })


    def __str__(self):
        return self.name


class OrderService(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_service = models.ForeignKey(Service, on_delete=models.CASCADE)
    order_service_admin = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="serviceadmin", on_delete=models.CASCADE)
    order_service_price = models.IntegerField()
    order_service_negotiate = models.BooleanField(default=False, null=True)
    order_service_negotiate_price = models.IntegerField(blank=True, null=True)
    order_service_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False, blank=True, null=True)
    active = models.BooleanField(default=False, blank=True, null=True)
    decline = models.BooleanField(default=False, blank=True, null=True)
    completed_by_user = models.BooleanField(default=False, blank=True, null=True)
    completed_by_provider = models.BooleanField(default=False, blank=True, null=True)
    completed = models.BooleanField(default=False, blank=True, null=True)
    service_admin_price = models.IntegerField(blank=True, default=00)
    paid = models.BooleanField(default=False, blank=True, null=True)
    ref_code = models.CharField(max_length=20)

    def accept_call_order(self):
        self.active= True
        self.decline= False

    def decline_call_order(self):
        self.decline= True
        self.active= False

    def service_user_confirmation(self):
        self.completed_by_user = True
        self.paid = True

        if self.completed_by_provider:
            self.completed = True

    def service_admin_confirmation(self):
        self.completed_by_provider = True

        if self.completed_by_user:
            self.completed = True

    def final_price(self):
        percentage_price = self.order_service_price * 0.06
        final = percentage_price + self.order_service_price
        return final

    def admin_price(self):
        percentage_price = self.order_service_price * 0.04
        admin_final = percentage_price - self.order_service_price
        return admin_final

    def get_paystack_verify_url(self):
        return reverse("service:paystackverify", kwargs={
            'ref': self.ref_code,
            'pk':self.pk,
        })



    def __str__(self):
        return f"{self.user} ordered {self.order_service.name} service"




