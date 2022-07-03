from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Service)
admin.site.register(OrderService)
admin.site.register(Category)

