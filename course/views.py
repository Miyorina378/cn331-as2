from django.shortcuts import render
from django.http import HttpRequest
from .models import Course

# Create your views here.
def courses(request: HttpRequest):
    course_database = Course.objects.all
    return render(request, 'course/courses.html', {'all':course_database})

def about(request: HttpRequest):
    return render(request, 'course/about.html')

