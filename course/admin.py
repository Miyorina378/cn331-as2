from django.contrib import admin
from .models import Course
# Register your models here.

class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_code', 'course_name','year','semester','seat','seat_is_full']
    search_fields = ['course_code']
admin.site.register(Course, CourseAdmin)
