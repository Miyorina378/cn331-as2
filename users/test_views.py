from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from course.models import Course
from users.forms import RegisterForm

class UserViewsTestCase(TestCase):

    def setUp(self):
        # Create a test user
        self.user = get_user_model().objects.create_user(username='testuser', password='password')
        self.course1 = Course.objects.create(course_code="CN101", course_name="Introductory Computer Programming", seat=10, seat_is_full=False)
        self.course2 = Course.objects.create(course_code="CN102", course_name="Programming Practice I", seat=0, seat_is_full=True)

    def test_register_view_get(self):
        """Test that the register view loads correctly (GET request)"""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertIsInstance(response.context['form'], RegisterForm)

    def test_register_view_post(self):
        """Test that a user can register successfully (POST request)"""
        form_data = {
            'username': 'newuser',
            'password1': 'complex_password_123',
            'password2': 'complex_password_123',
        }
        response = self.client.post(reverse('register'), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('courses'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_logout_view(self):
        """Test that a logged-in user can log out"""
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('courses'))

    def test_dashboard_view(self):
        """Test that the dashboard displays enrolled courses"""
        # Enroll the user in course1
        self.course1.Users.add(self.user)

        # Log in and access the dashboard
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('dashboard'))
        
        # Check if the dashboard loads correctly
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/dashboard.html')
        self.assertContains(response, 'Introductory Computer Programming')  # course1 should be listed

    def test_unenroll_from_dashboard_view(self):
        """Test unenrolling from a course via the dashboard"""
        # Enroll the user in course1
        self.course1.Users.add(self.user)

        # Log in and go to the dashboard
        self.client.login(username='testuser', password='password')
        dashboard_response = self.client.get(reverse('dashboard'))
        self.assertEqual(dashboard_response.status_code, 200)
        self.assertContains(dashboard_response, self.course1.course_name)

        # Unenroll from the course via the dashboard
        unenroll_response = self.client.post(reverse('unenroll_from_course', args=[self.course1.course_code]))

        # Check if the user is redirected to the dashboard after unenrollment
        self.assertRedirects(unenroll_response, reverse('dashboard'))

        # Ensure the user is no longer enrolled in course1
        self.course1.refresh_from_db()
        self.assertFalse(self.course1.Users.filter(id=self.user.id).exists())

        # Check if the seat count has increased
        self.assertEqual(self.course1.seat, 11)
        self.assertFalse(self.course1.seat_is_full)


    def test_unenroll_from_fulled_course(self):
        """Test unenrolling from a course that is full"""
        # Enroll the user in course2 (even though it's marked as full)
        self.course2.Users.add(self.user)
        self.course2.seat = 0
        self.course2.seat_is_full = True
        self.course2.save()
        # Log in as the user and try to unenroll from course2
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('unenroll_from_course', args=[self.course2.course_code]))

        # Check if the user is redirected to the dashboard
        self.assertRedirects(response, reverse('dashboard'))

        # Ensure the user is still not enrolled in course2 and no change seat count back to 1
        self.course2.refresh_from_db()
        self.assertFalse(self.course2.Users.filter(id=self.user.id).exists())
        self.assertEqual(self.course2.seat, 1)
        self.assertFalse(self.course2.seat_is_full)
