from django.urls import path
from .views import *

app_name='articles'
urlpatterns=[
    path('', index, name='index'),
]