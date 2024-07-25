from django.contrib import admin
from django.urls import path, include

from .views import *

#Define a list of url patterns
urlpatterns = [
    path('', home)
]
