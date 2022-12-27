
from django.urls import path,include
from .views import *

urlpatterns = [
    path('verify',verify,name='verify'),
    path('login',login,name='login'),
    path('register',register,name='register'),
    path('logout',logout_view,name='logout'),
    path('profile',profile,name='profile'),
    path('',home,name='home')
]
