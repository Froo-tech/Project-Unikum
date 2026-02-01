from django.urls import path
from .views import *

urlpatterns = [
    path("account/", account),
    path('account/logout/', logout, name='logout'),

]
