from django.db import models
from django.conf import settings
from django.utils import timezone
from django.shortcuts import reverse
# Create your models here.


class Category(models.Model):
    category = models.CharField(max_length=200)
    category_image = models.ImageField(blank=True, upload_to="Cat Image/")

    def __str_(self):
        return self.category