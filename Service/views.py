from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .models import *
from .forms import *
from django.utils import timezone
import random, string, requests, json
from Rendapp.settings import base
from Users.models import *
from django.contrib import messages
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from twilio.rest import Client
from django.core.mail import send_mail
from django.http import HttpResponse
# Create your views here.

tw_sid = base.account_sid
tw_token = base.auth_token
tw_num = base.my_number




def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


def order_sms(request, called_service):
    sender = UserProfile.objects.get(person =called_service.admin)
    sennum = sender.phone_number
    phone = str(sennum)
    account_sid = tw_sid
    auth_token = tw_token
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=f"Hi {called_service.name} admin, You have a new service order for your {called_service.category} service on rendapp. Kindly accept the order if you are interested ",
        from_='+12569608957',
        to= phone
    )

def admin_confirm_sms(request, called_service):
    sender = UserProfile.objects.get(person =called_service.user)
    sennum = sender.phone_number
    phone = str(sennum)
    account_sid = tw_sid
    auth_token = tw_token
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=f"Hi {called_service.order_service} admin, Your client has sucessfully closed the service you rendered with code {called_service.ref_code}. Kindly close this service from your end to receive your payment within the next 24 hours",
        from_='+12569608957',
        to= phone
    )

def client_confirm_sms(request, called_service):
    sender = UserProfile.objects.get(person =called_service.order_service.admin)
    sennum = sender.phone_number
    phone = str(sennum)
    account_sid = tw_sid
    auth_token = tw_token
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=f"Hi {request.user}, A provider has sucessfully closed the service you ordered with code {called_service.ref_code}. Kindly close this service from your end to enable your payment to provider within the next 24 hours",
        from_='+12569608957',
        to= phone
    )

class HomeView(View):
    def get(self, * args, **kwargs):
        category = Category.objects.all()[:6]
        context = {
            'categories': category,
        }
        return render(self.request, 'home.html', context)

# View function for creating a service
@login_required
def CreateService(request):
    if request.method == "POST":
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid:
            service = form.save(commit=False)
            service.admin = request.user
            service.created_date = timezone.now()
            service.save()
            return redirect('service:allservice')
        form = ServiceForm()
    else:
        form = ServiceForm()

    context = {
        'form': form
    }
    return render(request, 'service/addservice.html', context)


class ServiceListView(ListView):
    model = Service
    context_object_name = "services"
    template_name = "service/allservice.html"

    def get_queryset(self):
        return Service.objects.order_by('-created_date')


def servicedetail(request, pk, name):
    service = Service.objects.get(pk=pk, name=name)
    related_service = Service.objects.filter( category=service.category)
    related_list = [][:4]
    for item in related_service:
        if item.pk != service.pk:
            related_list.append(item)
    context = {
        'service': service,
        'related_list':related_list,
    }
    return render(request, 'service/servicedetail.html', context)

class CategoryListView(ListView):
    model = Category
    context_object_name = "categories"
    template_name = "service/categorylist.html"

    def get_queryset(self):
        return Category.objects.all()

def category(request, category):
    categories = Service.objects.filter(category=category)

    context = {
        'categories': categories,
        'category_name': category,
    }
    return render(request, 'service/category.html', context)

# View function to order a service
@login_required
def call_service(request, pk):
    # Get the service of the pk that is passed from the url
    called_service = get_object_or_404(Service, pk=pk)
    # Get a list of incomplete user service from DB
    order_qs = OrderService.objects.filter(
        user=request.user,
        order_service=called_service,
        ordered=True
    )
    if order_qs.exists():
        messages.info(request, f"YOU HAVE AN ACTIVE SERVICE ORDER WITH {called_service.name}")
        return redirect(called_service.get_detail())
    else:
        # create a service order if it doesnt exist
        order_service, created = OrderService.objects.get_or_create(
            order_service=called_service,
            user=request.user,
            admin = called_service.admin,
            order_service_date=timezone.now(),
            ordered=True,
            ref_code=create_ref_code()
        )
        order_sms(request, called_service)
        messages.info(request, f"YOU ORDERED {called_service.name} SERVICE")
        return redirect(called_service.get_detail())


@login_required
def accept_service_call(request, pk):
    logged_in_user = request.user
    ordered_service = get_object_or_404(
        OrderService,
        pk=pk,
        ordered=True,
    )
    if logged_in_user == ordered_service.order_service.admin:
        ordered_service.accept_call_order()
        ordered_service.save()
        messages.info(request, f"YOU ACCEPTED A NEW SERVICE ORDER. IT WILL BE ADDED TO YOUR ACTIVE  SERVICES ")
        return redirect('service:home')

@login_required
def decline_service_call(request, pk):
    logged_in_user = request.user
    ordered_service = get_object_or_404(
        OrderService,
        pk=pk,
        ordered=True,
    )
    if logged_in_user == ordered_service.order_service.admin:
        ordered_service.decline_call_order()
        ordered_service.save()
        messages.info(request, f"YOU DECLINED A SERVICE ORDER ")
        return redirect('service:home')

@login_required
def service_user_confirmation(request, pk, ref):
    logged_in_user = request.user
    ordered_service = get_object_or_404(
        OrderService,
        pk=pk,
        ref=ref,
        ordered=True,
        active =True,
    )
    if logged_in_user == ordered_service.user:
        ordered_service.service_user_confirmation()
        ordered_service.save()
        # todo, send a message to the provider that client has checked out the service
        admin_confirm_sms(ordered_service)
        messages.info(request, f"YOU HAVE SUCESSFULLY CLOSED {ordered_service.name} SERVICE. THE PROVIDER WILL BE NOTIFIED")
        return redirect('service:home')

@login_required
def service_admin_confirmation(request, pk, ref):
    logged_in_user = request.user
    ordered_service = get_object_or_404(
        OrderService,
        pk=pk,
        ref=ref,
        ordered=True,
        active=True,
    )
    if logged_in_user == ordered_service.order_service_admin:
        ordered_service.service_admin_confirmation()
        ordered_service.save()
        service, created = RenderedServices.objects.get_or_create(
            admin = logged_in_user,
            user = ordered_service.user,
            ordered_service = ordered_service.order_service,
            service_ordered_date = ordered_service.order_service_date,
            completed = ordered_service.completed,
            ref_code = ordered_service.ref_code,
        )
        # todo, send a message to the client that provider has checked out the service
        if ordered_service.completed:
            messages.info(request, f"YOU HAVE SUCESSFULLY CLOSED {ordered_service.name} SERVICE.")
        else:
            client_confirm_sms(ordered_service)
            messages.info(request, f"YOU HAVE SUCESSFULLY CLOSED {ordered_service.name} SERVICE. YOUR CLIENT WILL BE NOTIFIED")
        return redirect('service:home')


class SearchView(TemplateView):
    template_name = 'service/search.html'

def search_result(request):
    if request.method =="POST":
        service = request.POST['service']
        state = request.POST['state']
        city = request.POST['city']

        result = Service.objects.filter(
            name=service,
            service_state=state,
            service_city=city
        )
        context = {
            'searched_service': service,
            'searched_state': state,
            'result': result,
        }
        return render(request, 'service/searchresult.html', context)

class AboutView(TemplateView):
    template_name = 'service/about.html'

class ContactView(View):
    def get(self, *args, **kwargs):
        form = ContactForm()
        context = {
            'form': form,
        }
        return render(self.request,'service/contact.html', context)
    def post(self,*args, **kwargs):
        form = ContactForm(self.request.POST or None)
        if form.is_valid():
            EMAIL = form.cleaned_data.get('EMAIL')
            MESSAGE = form.cleaned_data.get('MESSAGE')
            NAME = form.cleaned_data.get('NAME')

            print(EMAIL, NAME, MESSAGE )
            send_mail(
                NAME,
                MESSAGE,
                EMAIL,
                ['vbellotech@gmail.com'],
                fail_silently=False,
            )
            return redirect('service:home')








