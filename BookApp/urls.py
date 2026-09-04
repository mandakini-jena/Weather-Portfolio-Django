from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('name/',views.name),
    path('calci/',views.cal),
    path('biodata/',views.bio),
    path('weather/',views.weatherdata)
]

