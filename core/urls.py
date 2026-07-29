from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("resources/", views.resources, name="resources"),
    path("sunshine/", views.sunshine, name="sunshine"),
    path("work/", views.work_list, name="work_list"),
    path("work/<slug:slug>/", views.work_detail, name="work_detail"),
    path("contact/", views.contact, name="contact"),
]
