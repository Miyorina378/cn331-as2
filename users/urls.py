from django.urls import include, path
from . import views

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("register", view=views.register, name="register"),
    path("logout_user", views.logout_user,name="logout"),
     path("dashboard", views.dashboard,name="dashboard"),
]