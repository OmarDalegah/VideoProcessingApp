from django.urls import path
from . import views

urlpatterns = [
    path('record_request', views.record_request),
]

