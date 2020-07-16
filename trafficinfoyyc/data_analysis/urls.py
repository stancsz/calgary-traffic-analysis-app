from django.urls import path
from data_analysis import views

urlpatterns = [
    path('', views.data_analysis, name='data_analysis'),
]