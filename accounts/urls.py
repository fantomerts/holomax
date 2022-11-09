from django.urls import path
 
from .views import register, profile
 
urlpatterns = [
    path('signup/', register, name='signup'),
    path('settings/',profile, name="profile")
]