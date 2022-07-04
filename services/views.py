from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .models import *
from .forms import *
from django.utils import timezone
import random, string
from django.conf import settings
from users.models import *
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.contrib import messages
from django.http import JsonResponse
import json
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail

paystack_key = settings.PAYSTACK_PUBLIC_KEY

#EMAILS TO SEND TO CUSTOMERS AND USERS
def order_email(request, pk):
    order = OrderService.objects.get(user=request.user, pk=pk, ordered=True)
    user_email = order.order_service_admin.email
    subject, from_email, to = 'YOU HAVE A NEW SERVICE ORDER ON RENDAPP', 'from@example.com', user_email
    text_content = 'YOUR SERVICE HAS BEEN ORDERED ON RENDAPP. ACCEPT THE ORDER OR DECLINE IN ORDER NOT TO WASTE THE CUSTOMERS TIME.'
    html_content = '<h2>VISIT YOUR RENDAPP TO ACCEPT SERVICE ORDER.</h2>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
# Create your views here.

class HomeView(View):
    def get(self, * args, **kwargs):
        category = Category.objects.all()[:8]
        context = {
            'category': category,
        }
        return render(self.request, 'home.html', context)

def servicedetail(request, pk):
    service = Service.objects.get(pk=pk)
    context = {
        'service': service
    }
    return render(request, 'service/servicedetail.html', context)

#class CategoryListView(ListView):
#    model = Category
#    context_object_name = "categories"
#    template_name = "service/categorylist.html"

 #   def get_queryset(self):
 #       return Category.objects.all()

def category(request, category):
    categories = Service.objects.filter(category=category)

    context = {
        'categor ies': categories,
        'category_name': category,
    }
    return render(request, 'service/category.html', context)

class ServiceListView(ListView):
    model = Service
    context_object_name = "services"
    template_name = "service/servicelist.html"

    def get_queryset(self):
        return Service.objects.order_by('-created_date')

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
            return redirect('service:list')
        form = ServiceForm()
    else:
        form = ServiceForm()

    context = {
        'form': form
    }
    return render(request, 'service/newservice.html', context)

def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))

def order_confirmation_email(request, pk):
    service = get_object_or_404(Service, pk=pk)
    admin_email = service.admin.email
    subject = "YOU HAVE A NEW SERVICE ORDER OFROM RENDAPP.IO"
    to = admin_email
    rendapp='admin@rendapp.com'

    ctx = {
        'user':request.user,
    }
    message = get_template('user/email.html').render(Context(ctx))
    msg = EmailMessage(subject, message, to=to, from_email=rendapp)
    msg.content_subtype = 'html'
    msg.send()

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
        return redirect('service:detail', pk =called_service.pk)
    else:
        # create a service order if it doesnt exist
        order_service, created = OrderService.objects.get_or_create(
            order_service=called_service,
            user=request.user,
            order_service_admin=called_service.admin,
            order_service_price=called_service.price,
            order_service_negotiate=called_service.negotiate,
            order_service_negotiate_price=called_service.price,
            order_service_date=timezone.now(),
            ordered=True,
            ref_code=create_ref_code()
        )
        #order_email(request, pk)
        return redirect('service:detail', pk =called_service.pk)

class ServiceAdminView(View, LoginRequiredMixin):
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            orders = OrderService.objects.filter(order_service_admin=self.request.user, ordered=True)
        else:
            return redirect('account_login')
        context = {
            'orders': orders
        }
        return render(self.request, 'service/service_admin.html', context)

@login_required
def accept_service_call(request, pk):
    logged_in_user = request.user
    ordered_service = get_object_or_404(
        OrderService,
        pk=pk,
        ordered=True,
    )
    if logged_in_user == ordered_service.order_service_admin:
        ordered_service.accept_call_order()
        ordered_service.save()
        return redirect('service:home')

@login_required
def decline_service_call(request, pk):
    logged_in_user = request.user
    ordered_service = get_object_or_404(
        OrderService,
        pk=pk,
        ordered=True,
    )
    if logged_in_user == ordered_service.order_service_admin:
        ordered_service.decline_call_order()
        ordered_service.save()
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
        service, created = OrderCompletedServices.objects.get_or_create(
            user=logged_in_user,
            ordered_service=ordered_service.order_service,
            negotiate=ordered_service.order_service_negotiate,
            service_ordered_date=ordered_service.order_service_date,
            service_price=ordered_service.order_service_price,
            completed_by_user=ordered_service.completed_by_user,
            user_paid=ordered_service.paid,
            ref_code=ordered_service.ref_code,
        )
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
            ordered_service = ordered_service.order_service,
            negotiate = ordered_service.order_service_negotiate ,
            service_ordered_date = ordered_service.order_service_date,
            service_price = ordered_service.order_service_price,
            completed_by_user = ordered_service.completed_by_user,
            completed_by_provider = ordered_service.completed_by_provider,
            user_paid = ordered_service.paid,
            ref_code = ordered_service.ref_code,
        )
        return redirect('service:home')


class PaystackView(View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderService.objects.get(
            user=self.request.user,
            ordered=True,
            pk=pk,
        )
        user = self.request.user
        amount = int(order.final_price())
        ref = order.ref_code
        
        context = {
            'service': order,
            'email': user.email,
            'amount': amount,
            'ref': ref,
        }
        return render(self.request, 'service/paystack.html', context)

class PaymentView(View):
    def get(self, *args, **kwargs):
        try:
            order = OrderService.objects.get(user=self.request.user, ordered=True, pk=pk, ref_code=ref)

            #messages.success(self.request, "order was successful")
            return redirect("/")
        except ObjectDoesNotExist:
            #messages.success(self.request, "Your order was successful")
            return redirect("/")



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
            'searched': service,
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
            #send_mail(
             #   NAME,
            #    MESSAGE,
             #   'from@example.com',
            #    [EMAIL],
             #   fail_silently=False,
            #)
            return redirect('service:home')