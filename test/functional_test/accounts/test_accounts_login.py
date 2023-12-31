from .base import AccountsBaseTest
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User
from django.urls import reverse


class AccountsLoginTest(AccountsBaseTest):
    def get_form(self):
        return self.browser.find_element(
            By.XPATH,
            '/html/body/div/div/div/form'
        )

    def test_user_valid_data_can_login_successfully(self):
        string_password = 'P@ssw0rd1'

        user = User.objects.create_user(
            username='my_user',
            password=string_password,
        )

        # Usuário abre a página de login
        self.browser.get(self.live_server_url + reverse('accounts:login'))

        # Usuário vê o formulário de login
        form = self.get_form()

        username_field = self.browser.find_element(By.NAME, 'username')
        password_field = self.browser.find_element(By.NAME, 'password')

        # Usuário digita seu usuário e senha
        username_field.send_keys(user.username)
        password_field.send_keys(string_password)

        # Usuário envia o formulário
        form.submit()

        # Usuário é redirecionado para o dashboard
        response = self.client.get(reverse('dashboard:home'))
        self.assertEqual(response.status_code, 302)

    def test_form_login_invalid_credentials(self):
        # Usuário abre a página de login
        self.browser.get(self.live_server_url + reverse('accounts:login'))

        # Usuário vê o formulário de login
        form = self.get_form()

        username_field = self.browser.find_element(By.NAME, 'username')
        password_field = self.browser.find_element(By.NAME, 'password')

        # E tenta enviar valores vazios
        username_field.send_keys(' ')
        password_field.send_keys(' ')

        # Envia o formulário
        form.submit()

        # Vê uma mensagem de erro na tela
        self.assertIn(
            'Invalid credentials.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_form_login_invalid_username_or_password(self):
        # Usuário abre a página de login
        self.browser.get(self.live_server_url + reverse('accounts:login'))

        # Usuário vê o formulário de login
        form = self.get_form()

        username_field = self.browser.find_element(By.NAME, 'username')
        password_field = self.browser.find_element(By.NAME, 'password')

        # E tenta enviar valores com dados que não correspondem
        username_field.send_keys('invalid_user')
        password_field.send_keys('invalid_password')

        # Envia o formulário
        form.submit()

        # Vê uma mensagem de erro na tela
        self.assertIn(
            'Invalid username or password.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_user_logged_cant_see_login_view(self):
        string_password = 'P@ssw0rd1'

        user = User.objects.create_user(
            username='my_user',
            password=string_password,
        )

        # Usuário abre a página de login
        self.browser.get(self.live_server_url + reverse('accounts:login'))

        # Usuário vê o formulário de login
        form = self.get_form()

        username_field = self.browser.find_element(By.NAME, 'username')
        password_field = self.browser.find_element(By.NAME, 'password')

        # Usuário digita seu usuário e senha
        username_field.send_keys(user.username)
        password_field.send_keys(string_password)

        # Usuário envia o formulário
        form.submit()

        # Usuário é redirecionado para o dashboard
        response = self.client.get(reverse('dashboard:home'))
        self.assertEqual(response.status_code, 302)

        # Usuário tenta acessar login novamente e
        # é redirecionado para o dashboard automaticamente
        self.browser.get(self.live_server_url + reverse('accounts:login'))
        self.assertEqual(response.status_code, 302)
