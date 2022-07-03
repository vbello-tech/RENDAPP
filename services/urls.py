from django.urls import path
from .views import *

app_name = "service"

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('service/<int:pk>/', servicedetail, name="detail"),
    path('services/', ServiceListView.as_view(), name="list"),
    path('services/category/', CategoryListView.as_view(), name="categorylist"),
    path('services/category/<str:category>/', category,name="category"),
    path('create-service/', CreateService, name="create"),
    path('call-service/<int:pk>/', call_service, name="call-service"),
    path('serviceorder/', ServiceAdminView.as_view(), name="serviceadmin"),
    #path('serviceorder/', serviceadmin, name="serviceadmin"),
    path('accept-service-call/<int:pk>/', accept_service_call, name="accept"),
    path('decline-service-call/<int:pk>/', decline_service_call, name="decline"),
    path('user-service-complete-confirmation/<int:pk>/', service_user_confirmation, name="user-confirm"),
    path('service_admin-service-completion-confirmation/<int:pk>/', service_admin_confirmation, name="admin-confirm"),
    path('service/payment/paystack/<int:pk>/', PaystackView.as_view(), name="paystack"),
    path('paystack-payment-verified/<str:ref>/<int:pk>/', PaymentView.as_view(), name="paystackverify"),
    path('services/search/', SearchView.as_view(), name="search"),
    path('services/search/result/', search_result, name="searchresult"),
    path('rendapp/about/', AboutView.as_view(), name="about"),
    path('rendapp/CONTACT/', ContactView.as_view(), name="contact"),
]