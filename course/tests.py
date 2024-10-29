from django.test import TestCase
from django.contrib.auth.models import User
from .models import Course, CourseEnrollment

class CourseTestCase(TestCase):

    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(username="user1", password="password123")
        self.user2 = User.objects.create_user(username="user2", password="password123")
        
        # Create courses
        self.course1 = Course.objects.create(
            course_code="CN101", 
            course_name="Introductory Computer Programming", 
            seat=2, 
            seat_is_full=False
        )
        
        self.course2 = Course.objects.create(
            course_code="CN102", 
            course_name="Programming Practice I", 
            seat=1, 
            seat_is_full=False
        )
    
    def test_course_str_method(self):
        """Test the __str__ method of the Course model"""
        expected_string = "CN101 | Introductory Computer Programming"
        self.assertEqual(str(self.course1), expected_string)

    def test_course_enrollment_str_method(self):
        """Test the __str__ method of the CourseEnrollment model"""
        # Create a course enrollment
        self.enrollment = CourseEnrollment.objects.create(user=self.user1, course=self.course1)

        expected_string = f"{self.user1.username} enrolled in {self.course1.course_code}"
        self.assertEqual(str(self.enrollment), expected_string)

    def test_course_enrollment(self):
        """Test if a user can successfully enroll in a course."""
        
        # Enroll user1 in course1
        enrolled = self.course1.enroll_student(self.user1)
        self.assertTrue(enrolled)
        self.assertEqual(self.course1.seat, 1)  # Check seat reduction
        
    def test_course_full(self):
        """Test that enrollment fails when course is full."""
        
        # Enroll user1 and user2 in course2
        self.course2.enroll_student(self.user1)
        self.course2.enroll_student(self.user2)
        
        # Course2 should be full now
        self.assertTrue(self.course2.seat_is_full)
        self.assertEqual(self.course2.seat, 0)

        # Try to enroll another user, should fail
        enrolled = self.course2.enroll_student(self.user2)
        self.assertFalse(enrolled)
        
    def test_double_enrollment_prevention(self):
        """Test that a user cannot enroll in the same course multiple times."""
        
        # Enroll user1 once
        enrolled_first_time = self.course1.enroll_student(self.user1)
        enrolled_second_time = self.course1.enroll_student(self.user1)
        
        # Ensure second enrollment fails
        self.assertTrue(enrolled_first_time)
        self.assertFalse(enrolled_second_time)

    def test_unenroll_from_course(self):
        """Test that a user can successfully unenroll from a course."""
        
        # Enroll user1 and then unenroll
        self.course1.enroll_student(self.user1)
        self.assertEqual(self.course1.seat, 1)

        # Unenroll user1
        enrollment = CourseEnrollment.objects.get(user=self.user1, course=self.course1)
        enrollment.delete()  # Simulate unenroll
        self.course1.seat += 1
        self.course1.save()

        self.assertEqual(self.course1.seat, 2)  # Seat should increase back
