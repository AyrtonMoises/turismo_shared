from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile


User = get_user_model()

class LoginViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.user = User.objects.create_user(
            email='teste@teste.com',
            password='123'
        )

    def tearDown(self):
        self.user.delete()

    def test_login_ok(self):
        """ Teste de login com credenciais corretas """
        response = self.client.get(self.login_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'contas/login.html')
        data = {'email': self.user.email, 'senha': '123'}
        response = self.client.post(self.login_url, data)
        redirect_url = reverse(settings.LOGIN_REDIRECT_URL)
        self.assertRedirects(response, redirect_url)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_error(self):
        """ Teste de login com credenciais incorretas """
        data = {'email': self.user.email, 'senha': '1234'}
        response = self.client.post(self.login_url, data)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'contas/login.html')

class CadastroViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('cadastro')
        self.model_user = User

    def test_cadastro_ok(self):
        """ Teste de cadastro de usuário """
        data = {
            'first_name': 'primeiro nome', 'last_name': 'sobrenome',
            'email': 'meuemail@email.com', 'password1': 'senhasecret4', 'password2': 'senhasecret4'
        }
        response = self.client.post(self.register_url, data)
        index_url = reverse('perfil')
        self.assertRedirects(response, index_url)
        self.assertEquals(self.model_user.objects.count(), 1)

    def test_cadastro_senhas_diferentes(self):
        """ Teste de cadastro de usuário com senhas diferentes """
        data = {
            'first_name': 'primeiro nome', 'last_name': 'sobrenome',
            'email': 'meuemail2@email.com', 'password1': 'senhasecret4', 'password2': 'senhasecret3'
        }
        response = self.client.post(self.register_url, data)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'contas/cadastro-usuario.html')
        self.assertEquals(self.model_user.objects.count(), 0)

    def test_cadastro_sem_email(self):
        """ Teste de cadastro de usuário com senhas diferentes """
        data = {
            'first_name': 'primeiro nome', 'last_name': 'sobrenome',
            'email': '', 'password1': 'senhasecret4', 'password2': 'senhasecret4'
        }
        response = self.client.post(self.register_url, data)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'contas/cadastro-usuario.html')
        self.assertEquals(self.model_user.objects.count(), 0)


class CadastroUpdateTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('perfil')
        self.user = User.objects.create_user(
            email='teste@teste.com',
            password='123'
        )

    def tearDown(self):
        self.user.delete()

    def test_update_perfil_ok(self):
        """ Teste atualizando dados de perfil do usuário """
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        foto = SimpleUploadedFile(
            'small.gif', small_gif, content_type='image/gif'
        )
        data = {
            'first_name': 'novo nome',
            'last_name': 'sobrenome novo',
            'email': 'teste_atualizado@teste.com',
            'biografia': 'Minha biografia de teste',
            'foto': foto,
            'facebook': 'https://facebook.com/perfil',
            'instagram': 'https://instagram.com/perfil',
            'twitter': 'https://twitter.com/perfil',
            'blog': 'https://meublog.com'
        }
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)
        self.client.login(email=self.user.email, password='123')
        response = self.client.post(self.url, data, format='multipart')
        self.assertRedirects(response, self.url)
        self.user.refresh_from_db()
        self.assertEquals(self.user.email, 'teste_atualizado@teste.com')
        self.assertEquals(self.user.first_name, 'novo nome')
        self.assertEquals(self.user.perfil.biografia, 'Minha biografia de teste')
        self.assertTrue(self.user.perfil.foto.url)
        self.assertEquals(self.user.perfil.facebook, 'https://facebook.com/perfil')
        self.assertEquals(self.user.perfil.instagram, 'https://instagram.com/perfil')
        self.assertEquals(self.user.perfil.twitter, 'https://twitter.com/perfil')
        self.assertEquals(self.user.perfil.blog, 'https://meublog.com')

    def test_update_user_error(self):
        """ Teste atualizando email com dado vazio """
        data = {'email': ''}
        self.client.login(email=self.user.email, password='123')
        response = self.client.post(self.url, data)
        self.assertFormError(response, 'form_user', 'email', 'Este campo é obrigatório.')
