from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('login/', views.loginPage, name='login'),
    path('create_user/', views.create_user, name='create_user'),
    path('view_orders/', views.view_orders, name='view_orders'),
    path('create_order/', views.create_order, name='create_order'),
    path('view_order_details/<int:order_id>/', views.view_order_details, name='view_order_details'),
    path('logout/', views.logout_view, name='logout'),    
]
