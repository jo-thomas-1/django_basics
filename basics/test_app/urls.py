from django.urls import path
from . import views # importing views module from current folder

urlpatterns = [
    path('', views.hello_world, name='test_app_hello')
]
