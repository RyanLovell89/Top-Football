from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    path('<int:product_id>/', views.product_information, name='product_information'),
    path('add/', views.add_product_to_store, name='add_product_to_store'),
]
