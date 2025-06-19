from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from .models import Cliente, Trabajador, Categoria

class UserRegistrationTests(TestCase):
    def setUp(self):
        self.client = Client()
        Group.objects.get_or_create(name='cliente')
        Group.objects.get_or_create(name='trabajador')
        # Any other groups needed for auth_error can be added later or in relevant test class

    def test_successful_cliente_registration(self):
        url = reverse('registro')
        data = {
            'email': 'cliente_reg_test@example.com', # Used as username
            'password1': 'TestPass123!',
            'password2': 'TestPass123!',
            'user_type': 'Cliente',
            'rut': '11111111-1',
            'nombre': 'Test Cliente Reg',
            'telefono': '+56911111111',
            # No Trabajador-specific fields
        }
        response = self.client.post(url, data)

        # Check user creation
        self.assertTrue(User.objects.filter(username='cliente_reg_test@example.com').exists())
        user = User.objects.get(username='cliente_reg_test@example.com')
        self.assertEqual(user.email, 'cliente_reg_test@example.com')

        # Check Cliente profile creation
        self.assertTrue(Cliente.objects.filter(user=user).exists())
        cliente = Cliente.objects.get(user=user)
        self.assertEqual(cliente.rut, '11111111-1')
        self.assertEqual(cliente.nombre, 'Test Cliente Reg')
        self.assertEqual(cliente.telefono, '+56911111111')
        self.assertEqual(cliente.email, user.email)

        # Check group assignment
        self.assertTrue(user.groups.filter(name='cliente').exists())
        self.assertFalse(user.groups.filter(name='trabajador').exists())

        # Check login status
        self.assertIn('_auth_user_id', self.client.session)
        self.assertEqual(int(self.client.session['_auth_user_id']), user.id)

        # Check redirection
        self.assertRedirects(response, reverse('inicio'), fetch_redirect_response=True) # Assuming 'inicio' is the target

    def test_successful_trabajador_registration(self):
        url = reverse('registro')
        # Create a Categoria for the area
        categoria_bodega, _ = Categoria.objects.get_or_create(nombre='Bodega')

        data = {
            'email': 'trabajador_reg_test@example.com', # Used as username
            'password1': 'TestPass123!',
            'password2': 'TestPass123!',
            'user_type': 'Trabajador',
            'rut': '22222222-2',
            'nombre': 'Test Trabajador Reg',
            'telefono': '+56922222222',
            'fecha_nacimiento': '1990-01-15',
            'direccion': 'Calle Falsa 123, Santiago',
            'area': 'Bodega' # Name of the Categoria
        }
        response = self.client.post(url, data)

        self.assertTrue(User.objects.filter(username='trabajador_reg_test@example.com').exists())
        user = User.objects.get(username='trabajador_reg_test@example.com')
        self.assertEqual(user.email, 'trabajador_reg_test@example.com')

        self.assertTrue(Trabajador.objects.filter(user=user).exists())
        trabajador = Trabajador.objects.get(user=user)
        self.assertEqual(trabajador.rut, '22222222-2')
        self.assertEqual(trabajador.nombre, 'Test Trabajador Reg')
        self.assertEqual(trabajador.telefono, '+56922222222')
        self.assertIsNotNone(trabajador.fecha_nacimiento)
        self.assertEqual(trabajador.direccion, 'Calle Falsa 123, Santiago')
        self.assertEqual(trabajador.area, categoria_bodega) # Check FK assignment

        self.assertTrue(user.groups.filter(name='trabajador').exists())
        self.assertFalse(user.groups.filter(name='cliente').exists())

        self.assertIn('_auth_user_id', self.client.session)
        self.assertEqual(int(self.client.session['_auth_user_id']), user.id)

        self.assertRedirects(response, reverse('inicio'), fetch_redirect_response=True)

    def test_registration_existing_email_as_username(self):
        # Create a user with the email that will be duplicated
        User.objects.create_user(username='existing@example.com', email='existing@example.com', password='password123')

        url = reverse('registro')
        data = {
            'email': 'existing@example.com', # Duplicate email/username
            'password1': 'TestPass123!',
            'password2': 'TestPass123!',
            'user_type': 'Cliente',
            'rut': '33333333-3',
            'nombre': 'Test Duplicado',
            'telefono': '+56933333333',
        }
        response = self.client.post(url, data)

        # Check user was not created (count should remain 1 for this username)
        self.assertEqual(User.objects.filter(username='existing@example.com').count(), 1)
        # Check form errors
        # The error comes from RegistroForm's clean_username or save method
        self.assertFormError(response.context['form'], 'email', 'A user with this email (username) already exists.') # Or specific field if error is attached elsewhere
        self.assertEqual(response.status_code, 200) # Should re-render the form

    def test_registration_mismatched_passwords(self):
        url = reverse('registro')
        data = {
            'email': 'mismatch@example.com',
            'password1': 'TestPass123!',
            'password2': 'DifferentPass123!', # Mismatched
            'user_type': 'Cliente',
            'rut': '44444444-4',
            'nombre': 'Test Mismatch',
            'telefono': '+56944444444',
        }
        response = self.client.post(url, data)

        self.assertFalse(User.objects.filter(username='mismatch@example.com').exists())
        # UserCreationForm handles this error
        self.assertFormError(response.context['form'], 'password2', "The two password fields didn’t match.")
        self.assertEqual(response.status_code, 200)

    def test_registration_missing_required_fields(self):
        url = reverse('registro')
        data = {
            'email': 'missing@example.com',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!',
            # user_type, rut, nombre, telefono are missing
        }
        response = self.client.post(url, data)

        self.assertFalse(User.objects.filter(username='missing@example.com').exists())
        self.assertFormError(response.context['form'], 'user_type', 'This field is required.')
        self.assertFormError(response.context['form'], 'rut', 'This field is required.')
        self.assertFormError(response.context['form'], 'nombre', 'This field is required.')
        self.assertFormError(response.context['form'], 'telefono', 'This field is required.')
        self.assertEqual(response.status_code, 200)

    # Additional registration tests will follow

class UserLoginLogoutTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_email = 'login_test@example.com'
        self.user_password = 'TestPass123!'
        # User is created with email as username, as per RegistroForm logic
        self.user = User.objects.create_user(username=self.user_email, email=self.user_email, password=self.user_password)

        # Assign user to a group for auth_error testing
        self.cliente_group, _ = Group.objects.get_or_create(name='cliente')
        self.user.groups.add(self.cliente_group)

    def test_login_correct_credentials(self):
        url = reverse('login') # Assuming 'login' maps to login_custom
        data = {
            'username': self.user_email, # AuthenticationForm expects 'username'
            'password': self.user_password,
        }
        response = self.client.post(url, data)

        self.assertIn('_auth_user_id', self.client.session)
        self.assertEqual(int(self.client.session['_auth_user_id']), self.user.id)
        # login_custom redirects to auth_error
        self.assertRedirects(response, reverse('auth_error'), fetch_redirect_response=False)

        # Test the subsequent redirect from auth_error
        auth_error_response = self.client.get(response.url) # Follow the redirect to /auth_error/
        # Since user is in 'cliente' group, auth_error redirects to 'inicio'
        self.assertRedirects(auth_error_response, reverse('inicio'), fetch_redirect_response=True)


    def test_login_incorrect_password(self):
        url = reverse('login')
        data = {
            'username': self.user_email,
            'password': 'WrongPassword!',
        }
        response = self.client.post(url, data)

        self.assertNotIn('_auth_user_id', self.client.session)
        self.assertEqual(response.status_code, 200) # Should re-render login page
        self.assertFormError(response.context['form'], None, 'Please enter a correct username and password. Note that both fields may be case-sensitive.')

    def test_login_non_existent_user(self):
        url = reverse('login')
        data = {
            'username': 'nonexistent@example.com',
            'password': 'somepassword',
        }
        response = self.client.post(url, data)

        self.assertNotIn('_auth_user_id', self.client.session)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], None, 'Please enter a correct username and password. Note that both fields may be case-sensitive.')

    def test_logout_user(self):
        # Log the user in first
        self.client.login(username=self.user_email, password=self.user_password)
        self.assertIn('_auth_user_id', self.client.session)

        # Access logout URL
        url = reverse('logout') # Assuming 'logout' maps to logout_usuario
        response = self.client.get(url)

        self.assertNotIn('_auth_user_id', self.client.session)
        self.assertRedirects(response, reverse('login'))

class AuthErrorRedirectTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_password = 'TestPass123!'
        self.auth_error_url = reverse('auth_error')

        # Create groups
        self.cliente_group, _ = Group.objects.get_or_create(name='cliente')
        self.trabajador_group, _ = Group.objects.get_or_create(name='trabajador')
        self.admin_group, _ = Group.objects.get_or_create(name='administrador_ferreteria')

        # Create users for each group
        self.cliente_user = User.objects.create_user(username='testcliente_auth@example.com', password=self.user_password)
        self.cliente_user.groups.add(self.cliente_group)

        self.trabajador_user = User.objects.create_user(username='testtrabajador_auth@example.com', password=self.user_password)
        self.trabajador_user.groups.add(self.trabajador_group)

        self.admin_user = User.objects.create_user(username='testadmin_auth@example.com', password=self.user_password)
        self.admin_user.groups.add(self.admin_group)

        self.no_group_user = User.objects.create_user(username='testnogroup_auth@example.com', password=self.user_password)

    def test_redirect_cliente(self):
        self.client.login(username=self.cliente_user.username, password=self.user_password)
        response = self.client.get(self.auth_error_url)
        self.assertRedirects(response, reverse('inicio')) # Cliente redirects to inicio ('/')

    def test_redirect_trabajador(self):
        self.client.login(username=self.trabajador_user.username, password=self.user_password)
        response = self.client.get(self.auth_error_url)
        self.assertRedirects(response, reverse('admin_trabajador'), fetch_redirect_response=False)

    def test_redirect_administrador_ferreteria(self):
        self.client.login(username=self.admin_user.username, password=self.user_password)
        response = self.client.get(self.auth_error_url)
        self.assertRedirects(response, reverse('admin_ferreteria'), fetch_redirect_response=False)

    def test_redirect_no_group_user(self):
        self.client.login(username=self.no_group_user.username, password=self.user_password)
        response = self.client.get(self.auth_error_url)
        self.assertRedirects(response, reverse('inicio')) # Users with no group redirect to inicio ('/')

    def test_redirect_unauthenticated_user(self):
        # User is not logged in
        response = self.client.get(self.auth_error_url)
        self.assertRedirects(response, reverse('login')) # auth_error redirects to login, doesn't add ?next itself
