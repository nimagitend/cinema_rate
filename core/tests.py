from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class RegistrationFlowTests(TestCase):
    def test_register_creates_regular_user_and_redirects_to_login(self):
        response = self.client.post(
            reverse('register'),
            {
                'email': 'user@example.com',
                'username': 'normal_user',
                'password1': 'StrongPass123',
                'password2': 'StrongPass123',
            },
            follow=True,
        )

        user_model = get_user_model()
        user = user_model.objects.get(username='normal_user')

        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(response.resolver_match.url_name, 'login')
        self.assertNotIn('_auth_user_id', self.client.session)


class LoginGuardTests(TestCase):
    def test_home_requires_authentication(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)