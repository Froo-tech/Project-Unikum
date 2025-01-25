from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.main),
    path('tracking_number', views.track),
    path("send/", views.send)

]
