from django.shortcuts import render
from django.http import HttpRequest
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def courses(request: HttpRequest):
    return render(request, 'course/courses.html')

def about(request: HttpRequest):
    return render(request, 'course/about.html')

