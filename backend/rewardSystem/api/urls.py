from django.urls import path
from . import views

urlpatterns = [
    path('login/student', views.loginStudent, name='loginStudent'),
    path('register', views.register, name='register')
]