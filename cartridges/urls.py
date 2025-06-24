from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('department/add/', views.add_department, name='add_department'),
    path('printer/add/', views.add_printer, name='add_printer'),
    path('cartridge/add/', views.add_cartridge, name='add_cartridge'),
    path('minstock/add/', views.set_min_stock, name='set_min_stock'),
    path('currentstock/add/', views.set_current_stock, name='set_current_stock'),
    path('order/', views.order, name='order'),
    path('stats/', views.stats, name='stats'),
    path('reference/', views.reference, name='reference'),
    path('history/', views.history, name='history'),
    path('compatibility/add/', views.add_compatibility, name='add_compatibility'),
]