from django.urls import path, include
from . import views

urlpatterns=[
    path("add/", views.AddClass.as_view()),
    path("", views.Class.as_view()),
]