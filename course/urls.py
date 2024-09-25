from django.urls import path
from . import views

urlpatterns = [path("", views.courses, name='courses'),
               path("about",views.about, name='about'),
               path('course/<str:course_code>/', views.course_detail, name='course_detail'),
               path('course/enroll/<int:course_id>/', views.enroll_in_course, name='enroll_in_course'),
               path('course/unenroll/<int:course_id>/', views.unenroll_from_course, name='unenroll_from_course'),]