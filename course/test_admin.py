from django.test import TestCase
from django.contrib.auth.models import User
from course.models import Course, CourseEnrollment
from django.contrib.admin.sites import AdminSite
from course.admin import CourseEnrollmentAdmin

# Mock request class for testing
class MockRequest:
    pass

class CourseEnrollmentAdminTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        
        self.course1 = Course.objects.create(course_code="CN101", course_name="Introductory Computer Programming", 
            course_description="test",
            semester="1",  
            year="2024",   
            seat=30,       
            seat_is_full=False  
        )
        self.enrollment1 = CourseEnrollment.objects.create(user=self.user, course=self.course1)
        self.admin_instance = CourseEnrollmentAdmin(model=CourseEnrollment, admin_site=AdminSite())

    def test_get_queryset_courses(self):
        """Test that get_queryset returns enrollments"""
        
        # Call the get_queryset method with a mock request
        queryset = self.admin_instance.get_queryset(MockRequest())
        self.assertIn(self.enrollment1, queryset)
        self.assertEqual(queryset.count(), 1)


