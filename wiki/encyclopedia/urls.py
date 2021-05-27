from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.show, name="page"), 
    path("add/", views.add, name="add"),
    path("random/", views.random, name="random"),
    path("edit/<str:title>", views.edit, name="edit")
]
