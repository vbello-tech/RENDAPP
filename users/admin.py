from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(RenderedServices)
admin.site.register(OrderCompletedServices)
admin.site.register(UserProfile)