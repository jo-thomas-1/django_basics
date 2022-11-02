from django.urls import path
from . import views # importing views module from current folder

urlpatterns = [
    path('', views.hello_world, name='test_app_hello'),
    path('add', views.pass_value, name='test_app_pass_value')
]
