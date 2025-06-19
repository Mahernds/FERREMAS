from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from .models import Cliente, Trabajador

class UserAuthTests(TestCase):

    def setUp(self):
        # Create groups if they don't exist (essential for registration)
        Group.objects.get_or_create(name='cliente')
        Group.objects.get_or_create(name='trabajador')
        self.client = Client()

    def test_successful_cliente_registration(self):
        # Define the registration URL
        url = reverse('registro')

        # Data for a new 'Cliente'
        data = {
            'username': 'testcliente',
            'email': 'testcliente@example.com',
            'password1': 'testpassword123', # Corrected from 'password'
            'password2': 'testpassword123',
            'user_type': 'Cliente',
            'rut': '12345678-9',
            'nombre': 'Test Cliente',
            'telefono': '+56912345678',
            # Optional fields for Cliente are not included
        }

        # Make a POST request to the registration view
        response = self.client.post(url, data)

        # Check if a new user was created
        self.assertTrue(User.objects.filter(username='testcliente').exists())
        user = User.objects.get(username='testcliente')

        # Check if a Cliente profile was created and linked to the user
        self.assertTrue(Cliente.objects.filter(user=user).exists())
        cliente = Cliente.objects.get(user=user)
        self.assertEqual(cliente.email, 'testcliente@example.com')
        self.assertEqual(cliente.rut, '12345678-9')
        self.assertEqual(cliente.nombre, 'Test Cliente')
        self.assertEqual(cliente.telefono, '+56912345678')

        # Check if the user was added to the 'cliente' group
        self.assertTrue(user.groups.filter(name='cliente').exists())

        # Check if the user is logged in (Django < 4.0: response.context['user'], Django >= 4.0 check _auth_user_id in session)
        # More robust: check if session has _auth_user_id after login
        self.assertIn('_auth_user_id', self.client.session)
        self.assertEqual(int(self.client.session['_auth_user_id']), user.id)

        # Check for redirect to 'inicio'
        self.assertRedirects(response, reverse('inicio'), fetch_redirect_response=True)

        # Check for success message (optional, but good practice)
        # messages = list(response.context['messages'])
        # self.assertEqual(len(messages), 1)
        # self.assertEqual(str(messages[0]), 'Cliente registrado con éxito.')
        # Note: Accessing messages directly in tests can be tricky.
        # It's often easier to check the redirect and model state.

    def test_successful_trabajador_registration(self):
        url = reverse('registro')
        data = {
            'username': 'testtrabajador',
            'email': 'testtrabajador@example.com',
            'password1': 'testpassword123', # Corrected from 'password'
            'password2': 'testpassword123',
            'user_type': 'Trabajador',
            'rut': '98765432-1',
            'nombre': 'Test Trabajador',
            'telefono': '+56987654321',
            'fecha_nacimiento': '1990-01-01', # Optional field
            'direccion': 'Calle Falsa 123',    # Optional field
            'area': 'Bodega'                   # Optional field
        }
        response = self.client.post(url, data)

        self.assertTrue(User.objects.filter(username='testtrabajador').exists())
        user = User.objects.get(username='testtrabajador')

        self.assertTrue(Trabajador.objects.filter(user=user).exists())
        trabajador = Trabajador.objects.get(user=user)
        self.assertEqual(trabajador.email, 'testtrabajador@example.com')
        self.assertEqual(trabajador.rut, '98765432-1')
        self.assertEqual(trabajador.nombre, 'Test Trabajador')
        self.assertEqual(trabajador.telefono, '+56987654321')
        self.assertIsNotNone(trabajador.fecha_nacimiento) # Check if date was saved
        self.assertEqual(trabajador.direccion, 'Calle Falsa 123')
        self.assertEqual(trabajador.area, 'Bodega')

        self.assertTrue(user.groups.filter(name='trabajador').exists())
        self.assertIn('_auth_user_id', self.client.session)
        self.assertEqual(int(self.client.session['_auth_user_id']), user.id)
        self.assertRedirects(response, reverse('inicio'), fetch_redirect_response=True)

    def test_registration_existing_username(self):
        # Create a user first
        User.objects.create_user(username='existinguser', password='password123', email='existing@example.com')

        url = reverse('registro')
        data = {
            'username': 'existinguser', # Same username
            'email': 'testcliente2@example.com',
            'password': 'testpassword123',
            'password2': 'testpassword123',
            'user_type': 'Cliente',
            'rut': '12345678-0',
            'nombre': 'Test Cliente 2',
            'telefono': '+56912345670',
        }
        response = self.client.post(url, data)

        # Check that no new user with this username was created (count should remain 1)
        self.assertEqual(User.objects.filter(username='existinguser').count(), 1)
        # Check that the form contains errors (UserCreationForm adds errors for duplicate username)
        self.assertFormError(response.context['form'], 'username', 'A user with that username already exists.')
        # Check that the response is 200 (returns to registration page)
        self.assertEqual(response.status_code, 200)

    def test_registration_missing_required_fields(self):
        url = reverse('registro')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            # Missing password, user_type, rut, nombre, telefono
        }
        response = self.client.post(url, data)

        # Check that no user was created
        self.assertFalse(User.objects.filter(username='newuser').exists())
        # Check that the form contains errors for multiple fields
        self.assertFormError(response.context['form'], 'password1', 'This field is required.') # Corrected field and message
        self.assertFormError(response.context['form'], 'user_type', 'This field is required.')
        self.assertFormError(response.context['form'], 'rut', 'This field is required.')
        self.assertFormError(response.context['form'], 'nombre', 'This field is required.')
        self.assertFormError(response.context['form'], 'telefono', 'This field is required.')
        # Check that the response is 200
        self.assertEqual(response.status_code, 200)

class UserLoginLogoutTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create a user for login tests
        self.username = 'testloginuser'
        self.email = 'testlogin@example.com'
        self.password = 'testpassword123'
        self.user = User.objects.create_user(username=self.username, email=self.email, password=self.password)
        cliente_group, _ = Group.objects.get_or_create(name='cliente')
        self.user.groups.add(cliente_group)
        # Create other groups if needed for more specific auth_error tests
        Group.objects.get_or_create(name='trabajador')
        Group.objects.get_or_create(name='administrador_ferreteria')


    def test_login_correct_credentials(self):
        url = reverse('login')
        data = {
            'username': self.username, # AuthenticationForm uses 'username'
            'password': self.password,
        }
        response = self.client.post(url, data)

        self.assertIn('_auth_user_id', self.client.session)
        self.assertEqual(int(self.client.session['_auth_user_id']), self.user.id)

        # Check the first redirect to auth_error
        # response.url from a redirect might not have the trailing slash,
        # but reverse('auth_error') will (due to APPEND_SLASH behavior and urls.py definition)
        # So, we expect the redirect location to be exactly what reverse() gives.
        self.assertRedirects(response, expected_url=reverse('auth_error'), fetch_redirect_response=False)

        # Follow the redirect from auth_error (since user is in 'cliente' group, it should go to 'inicio')
        # response.url here will be the location header from the previous response.
        auth_error_response = self.client.get(response.url)
        self.assertRedirects(auth_error_response, reverse('inicio'), fetch_redirect_response=True)


    def test_login_incorrect_password(self):
        url = reverse('login')
        data = {
            'username': self.username,
            'password': 'wrongpassword',
        }
        response = self.client.post(url, data)

        self.assertNotIn('_auth_user_id', self.client.session) # Should not be logged in
        self.assertEqual(response.status_code, 200) # Returns to login page
        self.assertFormError(response.context['form'], None, 'Please enter a correct username and password. Note that both fields may be case-sensitive.')

    def test_login_non_existent_user(self):
        url = reverse('login')
        data = {
            'username': 'nonexistentuser',
            'password': 'somepassword',
        }
        response = self.client.post(url, data)

        self.assertNotIn('_auth_user_id', self.client.session)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], None, 'Please enter a correct username and password. Note that both fields may be case-sensitive.')

    def test_user_logout(self):
        # First, log in the user
        self.client.login(username=self.username, password=self.password)
        self.assertIn('_auth_user_id', self.client.session)

        # Then, access the logout URL
        logout_url = reverse('logout') # Assuming 'logout' is the name for user_logout or logout_usuario
                                       # Based on urls.py, 'logout' maps to logout_usuario
                                       # and user_logout was modified to redirect to 'login'
                                       # For consistency with the subtask focusing on login_custom and user_logout
                                       # let's assume we should test the one named 'logout' that redirects to 'login'

        # Let's check urls.py again. `user_logout` is not named. `logout_usuario` is named 'logout'.
        # The previous subtask modified `user_logout` to redirect to 'login'.
        # And `logout_usuario` also redirects to 'login'.
        # It's better to have one logout view. For now, I'll test 'logout_usuario' as it's named.

        response = self.client.get(logout_url)

        self.assertNotIn('_auth_user_id', self.client.session)
        self.assertRedirects(response, reverse('login'))

    # Example of how to check messages if needed (requires extra setup or checking response content)
    # def test_registration_success_message(self):
    #     url = reverse('registro')
    #     data = {
    #         'username': 'testclientemsg', 'email': 'testclientemsg@example.com',
    #         'password': 'password123', 'password2': 'password123', 'user_type': 'Cliente',
    #         'rut': '11111111-1', 'nombre': 'Test Msg', 'telefono': '1234567'
    #     }
    #     response = self.client.post(url, data, follow=True) # follow=True to get the final page with messages
    #     self.assertContains(response, "Cliente registrado con éxito.")

# More test classes or methods can be added below
