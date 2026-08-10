from django.contrib import admin
from django.urls import path
from voting import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("vote/", views.vote, name="vote"),
    path("success/", views.success, name="success"),
    path("results/", views.results, name="results"),
    path("health/", views.health, name="health"),
]
