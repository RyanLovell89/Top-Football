from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    path('<int:product_id>/', views.product_information, name='product_information'),
    path('add/', views.add_product_to_store, name='add_product_to_store'),
    path('edit/<int:product_id>/', views.edit_product_on_store, name='edit_product_on_store'),
    path('delete/<int:product_id>/', views.delete_product_on_store, name='delete_product_on_store'),
]
