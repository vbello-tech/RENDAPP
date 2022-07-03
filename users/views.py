from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import *
from services.models import *

# Create your views here.

class AdminRenderedView(View, LoginRequiredMixin):
    def get(self, *args, **kwargs):
        orders = RenderedServices.objects.filter(
            admin=self.request.user,
            completed_by_user = True,
            completed_by_provider = True,
        )
        context = {
            'orders': orders
        }
        return render(self.request, 'user/renderedservices.html', context)

class UserCompletedView(View, LoginRequiredMixin):
    def get(self, *args, **kwargs):
        orders = OrderCompletedServices.objects.filter(
            user=self.request.user,
            completed_by_user = True,
            completed_by_provider = True,
        )
        context = {
            'orders': orders
        }
        return render(self.request, 'user/completedservices.html', context)