from .adiospace import views
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("polls/", views.index, name="index"),
    path("admin/", admin.site.urlts)
]
