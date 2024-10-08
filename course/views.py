from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.contrib import messages
from .models import Course, CourseEnrollment
from django.contrib.auth.decorators import login_required

# Retrieve all courses 
course_database = Course.objects.all

def courses(request: HttpRequest):
    return render(request, 'course/courses.html', {'all': course_database})

def about(request: HttpRequest):
    return render(request, 'course/about.html')

def course_detail(request, course_code):
    single_course = get_object_or_404(Course, course_code=course_code)
    return render(request, 'course/course_detail.html', context={'single_course': single_course})

@login_required
def enroll_in_course(request, course_code):
    course = get_object_or_404(Course, course_code=course_code)

    if request.method == 'POST':
        if course.enroll_student(request.user):
            messages.success(request, "You have successfully enrolled in the course.")
        else:
            messages.error(request, "Enrollment failed. The course may be full or you may already be enrolled.")
    return redirect('courses')

@login_required
def unenroll_from_course(request, course_code):
    course = get_object_or_404(Course, course_code=course_code)

    if request.method == 'POST':
        course.unenroll_student(request.user)
    return redirect('courses')

