from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_bag, name='view_bag'),
    path('add/<item_id>/', views.add_to_bag, name='add_to_bag'),
    path('update/<item_id>/', views.update_to_bag, name='update_to_bag'),
    path('delete/<item_id>/', views.delete_from_bag, name='delete_from_bag'),
]
