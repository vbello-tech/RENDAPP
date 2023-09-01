from django.urls import path
from .views import *

app_name = "user"

urlpatterns = [
    path('services-rendered/', ServiceView.as_view(), name="service"),
    path('add-profile/', CreateProfileView.as_view(), name="addprofile"),
    path('profile', ProfileView.as_view(), name="profile"),
    path('artisans/onboarding/', onboarduser, name="onboard"),
    path('signup/artisan/', artisan_signup_view, name="artisan_sign_up"),
]