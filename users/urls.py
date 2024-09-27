from django.urls import include, path
from . import views

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("register", view=views.register, name="register"),
    path("logout_user", views.logout_user,name="logout"),
    path("dashboard", views.dashboard,name="dashboard"),
    path('unenroll/<str:course_code>/', views.unenroll_from_course, name='unenroll_from_course'),
]