from django.urls import path
from . import views

urlpatterns = [
    path('', views.profiles, name='profiles'),
    path('order_history/<order_number>', views.profiles, name='order_history'),
]
