from django.urls import path
from .views import *

app_name = "user"

urlpatterns = [
    path('services-rendered/', AdminRenderedView.as_view(), name="rendered"),
    path('services-completed/', UserCompletedView.as_view(), name="completed"),
    path('add-profile/', CreateProfile, name="addprofile"),
    path('profile', ProfileView.as_view(), name="profile"),

]