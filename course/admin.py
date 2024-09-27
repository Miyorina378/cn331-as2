from django.contrib import admin
from .models import Course, CourseEnrollment
# Register your models here.

class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_code', 'course_name','year','semester','seat','seat_is_full']
    search_fields = ['course_code']
    sortable_by = ['course_code', 'course_name','year','semester','seat','seat_is_full']
class CourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'enroll_date']
    search_fields = ['course']
    sortable_by = ['user', 'course', 'enroll_date']
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseEnrollment, CourseEnrollmentAdmin)
