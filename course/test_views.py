from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from .models import Course, CourseEnrollment

class CourseViewsTestCase(TestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password')
        self.staff_user = User.objects.create_user(username='staffuser', password='password', is_staff=True)

        # Create test courses
        self.course1 = Course.objects.create(course_code="CN101", course_name="Introductory Computer Programming", seat=10, seat_is_full=False)
        self.course2 = Course.objects.create(course_code="CN102", course_name="Programming Practice I", seat=0, seat_is_full=True)
        self.course3 = Course.objects.create(course_code="CN202", course_name="Data Structure & Algorithm 1", seat = 3, seat_is_full = True)

    def test_courses_view(self):
        """Test that the courses view loads correctly"""
        response = self.client.get(reverse('courses'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Introductory Computer Programming")
        self.assertContains(response, "Programming Practice I")

    def test_about_view(self):
        """Test that the about view loads correctly"""
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_course_detail_view(self):
        """Test the course detail view"""
        response = self.client.get(reverse('course_detail', args=[self.course1.course_code]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Introductory Computer Programming")

    def test_enroll_in_course_view(self):
        """Test enrolling in a course"""
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('enroll_in_course', args=[self.course1.course_code]))
        self.assertRedirects(response, reverse('courses'))
        
        # Check if the user is enrolled
        self.course1.refresh_from_db()
        self.assertTrue(CourseEnrollment.objects.filter(user=self.user, course=self.course1).exists())

        # Check success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "You have successfully enrolled in the course.")

    def test_enroll_in_full_course(self):
        """Test enrolling in a full course fails"""
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('enroll_in_course', args=[self.course2.course_code]))
        self.assertRedirects(response, reverse('courses'))

        # Check that enrollment failed
        self.course2.refresh_from_db()
        self.assertFalse(CourseEnrollment.objects.filter(user=self.user, course=self.course2).exists())

        # Check error message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Enrollment failed. The course may be full or you may already be enrolled.")
    
    def test_enroll_in_closed_course(self):
        """Test that enrolling in a closed course fails"""
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('enroll_in_course', args=[self.course3.course_code]))
        self.assertRedirects(response, reverse('courses'))

        # Check that enrollment failed
        self.course2.refresh_from_db()
        self.assertFalse(CourseEnrollment.objects.filter(user=self.user, course=self.course3).exists())
        
        # Check error message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Enrollment failed. The course may be full or you may already be enrolled.")

    def test_staff_access(self):
        """Test that staff user can access all course details"""
        self.client.login(username='staffuser', password='password')
        response = self.client.get(reverse('course_detail', args=[self.course1.course_code]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Introductory Computer Programming")

