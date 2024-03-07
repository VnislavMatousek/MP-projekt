from django.urls import path, include

from . import views

from .views import calculate_tax



urlpatterns = [
    path("", views.index, name="index"),
    path('calculate/', calculate_tax, name='calculate_tax'),
    path('calculaterok/', views.calculate_tax_rok, name='calculate_tax2'),
    path('novinky/', views.novinky, name='novinky'),
    path('history/', views.history, name='result_history'),
    path("account/registration/", views.registration, name="registration")
]
