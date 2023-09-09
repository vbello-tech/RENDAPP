from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from Service.models import Category

class HomeView(View):
    def get(self, * args, **kwargs):
            category = Category.objects.all()[:6]
            context = {
                'categories': category,
            }
            return render(self.request, 'home.html', context)