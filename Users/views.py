from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import *
from Service.models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from Service.models import OrderService

# Create your views here.

class AdminRenderedView(View, LoginRequiredMixin):
    def get(self, *args, **kwargs):
        orders = RenderedServices.objects.filter(
            admin=self.request.user,
            completed = True,
        )
        context = {
            'orders': orders
        }
        return render(self.request, 'user/renderedservices.html', context)

class UserCompletedView(View, LoginRequiredMixin):
    def get(self, *args, **kwargs):
        orders = OrderService.objects.filter(
            user=self.request.user,
            completed = True,
        )
        context = {
            'orders': orders
        }
        return render(self.request, 'user/completedservices.html', context)


# View function for creating a service
def CreateProfile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid:
            profile = form.save(commit=False)
            profile.person = request.user
            profile.save()
            return redirect('user:profile')
        form = ProfileForm()
    else:
        form = ProfileForm()

    context = {
        'form': form
    }
    return render(request, 'user/addprofile.html', context)


class ProfileView(View, LoginRequiredMixin):
    def get(self, *args, **kwargs):
        try:
            profile = UserProfile.objects.filter(
                person=self.request.user,
            )
            context = {
                'profile': profile
            }
            return render(self.request, 'user/profile.html', context)
        except ObjectDoesNotExist:
            return redirect('user:addprofile')

def artisan_signup_view(request):
    if request.method == 'POST':
        form = NewUSerForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('user:onboard')
    else:
        form = NewUSerForm()

    context = {
        'form': form
    }
    return render(request, 'user/artisan_signup.html', context)


# View function for creating a service
@login_required
def onboarduser(request):
    if request.method == "POST":
        form = OnboardForm(request.POST, request.FILES)
        if form.is_valid:
            service = form.save(commit=False)
            service.admin = request.user
            service.created_date = timezone.now()
            service.save()
            return redirect('user:profile')
        form = OnboardForm()
    else:
        form = OnboardForm()

    context = {
        'form': form
    }
    return render(request, 'user/onboard.html', context)


def handler404(request, exception):
    context = {"<h1>PAGE NOT FOUND!! ARE YOU SURE YOU ARE NAVIGATING TO THE RIGHT PAGE?</h1>"}
    response = render(request, "Templates/404.html", context)
    response.status_code = 404
    return response


def handler500(request):
    context =  {"<h1>OOPS !!! <br> SEVER ERROR!!! <br> </h1>"}
    response = render(request, "Templates/500.html", context)
    response.status_code = 500
    return response