from django.urls import path
from . import views
urlpatterns=[
    path('bill',views.bill_items,name='index'),
    path('add',views.add_products,name='add'),
    path('delete',views.delete_products,name='delete'),
    path('products',views.Total_products,name='products'),
    path('sales',views.Total_sales,name='sales'),
    path('update',views.update_products,name='update'),
    path('',views.dashboard,name='dashboard')
]