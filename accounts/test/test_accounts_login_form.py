from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class AccountsLoginForm(TestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'User',
            'password': '@Bc123456',
        }
        return super().setUp(*args, **kwargs)

    def test_user_can_login_succesfully(self):
        login_url = reverse('accounts:login')
        dashboard_url = reverse('dashboard:home')

        User.objects.create_user(
            username=self.form_data['username'],
            password=self.form_data['password'],
        )

        response = self.client.post(
            login_url,
            data=self.form_data,
            follow=True,
        )

        self.assertRedirects(response, dashboard_url)

    def test_user_cant_login_succesfully(self):
        url = reverse('accounts:login')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn('Invalid username or password.',
                      response.content.decode('utf-8'))
