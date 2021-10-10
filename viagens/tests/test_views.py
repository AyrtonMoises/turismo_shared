from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from viagens.models import Comentario, PontoTuristico, Viagem

User = get_user_model()


# class CadastroViagemTestCase(TestCase):

#     def setUp(self):
#         self.client = Client()
#         self.url_minhas_viagens = reverse('minhas-viagens')
#         self.url_cadastro_viagem = reverse('cadastrar-viagem')
#         self.url_login = reverse(settings.LOGIN_URL)
#         self.user = User.objects.create_user(
#             email='teste@teste.com',
#             password='senha_secreta'
#         )
#         small_gif = (
#             b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
#             b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
#             b'\x02\x4c\x01\x00\x3b'
#         )
#         self.foto = SimpleUploadedFile(
#             'small.gif', small_gif, content_type='image/gif'
#         )

#     def tearDown(self):
#         self.user.delete()
#         Viagem.objects.all().delete()

#     def test_acesso_lista_minhas_viagens(self):
#         """ Teste de acesso a Minhas Viagens """
#         response = self.client.get(self.url_minhas_viagens)
#         self.assertRedirects(response, self.url_login + f"?next={self.url_minhas_viagens}")
#         self.client.login(email=self.user.email, password='senha_secreta')
#         response = self.client.get(self.url_minhas_viagens)
#         self.assertEquals(response.status_code, 200)
#         self.assertTemplateUsed(response, 'viagens/cadastro/minhas-viagens.html')

#     def test_acesso_cadastro_viagem(self):
#         """ Teste de acesso a Cadastro de viagem """
#         response = self.client.get(self.url_cadastro_viagem)
#         self.assertRedirects(response, self.url_login + f"?next={self.url_cadastro_viagem}")
#         self.client.login(email=self.user.email, password='senha_secreta')
#         response = self.client.get(self.url_cadastro_viagem)
#         self.assertEquals(response.status_code, 200)
#         self.assertTemplateUsed(response, 'viagens/cadastro/cadastro-viagem.html')

#     def test_cadastrar_viagem_ok(self):
#         """ Teste cadastrando uma viagem """
#         self.client.login(email=self.user.email, password='senha_secreta')
#         data = {
#             'titulo': 'Meu titulo de viagem',
#             'localidade': 'localidade, estado - (País)',
#             'resumo': """Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#                 Curabitur vel efficitur quam, id gravida leo. Integer vel ex vel quam bibendum cursus nec a erat.
#                 Maecenas sed lobortis risus, lacinia gravida sapien.
#                 Suspendisse malesuada id dolor quis pretium""",
#             'avaliacao': 5,
#             'ativo': True,
#             'foto': self.foto
#         }
#         response = self.client.post(self.url_cadastro_viagem, data, format='multipart')
#         self.assertEquals(response.status_code, 302)
#         self.assertRedirects(response, self.url_minhas_viagens)

#     def test_cadastrar_viagem_error(self):
#         """ Teste cadastrando uma viagem """
#         self.client.login(email=self.user.email, password='senha_secreta')

#         data = {
#             'titulo': '',
#             'localidade': '',
#             'resumo': '',
#             'avaliacao': 999,
#             'ativo': True
#         }
#         response = self.client.post(self.url_cadastro_viagem, data, format='multipart')
#         self.assertFormError(response, 'form', 'titulo', 'Este campo é obrigatório.')
#         self.assertFormError(response, 'form', 'localidade', 'Este campo é obrigatório.')
#         self.assertFormError(response, 'form', 'resumo', 'Este campo é obrigatório.')
#         self.assertFormError(response, 'form', 'foto', 'Este campo é obrigatório.')
#         self.assertFormError(response, 'form', 'avaliacao', 'Faça uma escolha válida. 999 não é uma das escolhas disponíveis.')

#     def test_atualizar_viagem_ok(self):
#         """ Teste atualizando cadastro de viagem """
#         viagem = Viagem.objects.create(
#             titulo = 'Uma viagem',
#             localidade = 'São Paulo, SP - Brasil',
#             foto = 'foto_viagem.jpg',
#             resumo = 'Um bom lugar para se visitar',
#             ativo = True,
#             avaliacao = 3,
#             user = self.user
#         )
#         self.client.login(email=self.user.email, password='senha_secreta')
#         data = {
#             'titulo': 'Novo titulo',
#             'localidade': 'Nova localidade',
#             'resumo': 'Novo resumo',
#             'avaliacao': 3,
#             'foto': self.foto,
#             'ativo': False
#         }
#         response = self.client.post(reverse('editar-viagem', kwargs={'pk': viagem.id}), data, format='multipart')
#         self.assertEquals(response.status_code, 302)
#         self.assertRedirects(response, reverse('editar-viagem', kwargs={'pk': viagem.id}))
#         viagem.refresh_from_db()
#         self.assertEquals(viagem.titulo, 'Novo titulo')
#         self.assertEquals(viagem.localidade, 'Nova localidade')
#         self.assertEquals(viagem.resumo, 'Novo resumo')
#         self.assertEquals(viagem.avaliacao, 3)
#         self.assertEquals(viagem.ativo, False)

#     def test_atualizar_viagem_error(self):
#         """ Teste atualizando cadastro de viagem com erro """
#         viagem = Viagem.objects.create(
#             titulo = 'Uma viagem',
#             localidade = 'São Paulo, SP - Brasil',
#             foto = 'foto_viagem.jpg',
#             resumo = 'Um bom lugar para se visitar',
#             ativo = True,
#             avaliacao = 3,
#             user = self.user
#         )
#         self.client.login(email=self.user.email, password='senha_secreta')

#         data = {
#             'titulo': '',
#             'resumo': '',
#             'avaliacao': 999,
#         }
#         response = self.client.post(reverse('editar-viagem', kwargs={'pk': viagem.id}), data, format='multipart')
#         self.assertFormError(response, 'form', 'titulo', 'Este campo é obrigatório.')
#         self.assertFormError(response, 'form', 'resumo', 'Este campo é obrigatório.')
#         self.assertFormError(response, 'form', 'avaliacao', 'Faça uma escolha válida. 999 não é uma das escolhas disponíveis.')

#     def test_deletar_viagem(self):
#         """ Teste deletar viagem cadastrada """
#         viagem = Viagem.objects.create(
#             titulo = 'Uma viagem',
#             localidade = 'São Paulo, SP - Brasil',
#             foto = 'foto_viagem.jpg',
#             resumo = 'Um bom lugar para se visitar',
#             ativo = True,
#             avaliacao = 3,
#             user = self.user
#         )
#         url_deletar_viagem = reverse('deletar-viagem', kwargs={'pk': viagem.id})
#         response = self.client.get(url_deletar_viagem)
#         self.assertRedirects(response, self.url_login + f"?next={url_deletar_viagem}")
#         self.client.login(email=self.user.email, password='senha_secreta')
#         response = self.client.get(url_deletar_viagem)
#         self.assertEquals(response.status_code, 200)
#         self.assertTemplateUsed(response, 'viagens/cadastro/deletar-viagem.html')
#         response = self.client.post(url_deletar_viagem)
#         self.assertEquals(Viagem.objects.count(), 0)


# class HomeTestCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.url_home = reverse('home')
#         self.user = User.objects.create_user(
#             email='teste@teste.com',
#             password='senha_secreta'
#         )

#         self.viagem1 = Viagem.objects.create(
#             titulo = 'Primeira viagem',
#             localidade = 'São Paulo, SP - Brasil',
#             foto = 'foto_viagem.jpg',
#             resumo = 'Um bom lugar para se visitar',
#             ativo = True,
#             avaliacao = 3,
#             user = self.user
#         )
#         self.viagem2 = Viagem.objects.create(
#             titulo = 'Segunda viagem',
#             localidade = 'São Paulo, SP - Brasil',
#             foto = 'foto_viagem.jpg',
#             resumo = 'Um bom lugar para se visitar',
#             ativo = True,
#             avaliacao = 3,
#             user = self.user
#         )
#         self.viagem3 = Viagem.objects.create(
#             titulo = 'Terceira viagem',
#             localidade = 'São Paulo, SP - Brasil',
#             foto = 'foto_viagem.jpg',
#             resumo = 'Um bom lugar para se visitar',
#             ativo = True,
#             avaliacao = 3,
#             user = self.user
#         )

#     def tearDown(self):
#         self.user.delete()
#         Viagem.objects.all().delete()

#     def test_acesso_home(self):
#         """ Teste de acesso a Minhas Viagens """
#         response = self.client.get(self.url_home)
#         self.assertEquals(response.status_code, 200)
#         self.assertTemplateUsed(response, 'home/index.html')

#     def test_destaques_home(self):
#         """
#         Testar exibição e ordem de viagens em
#         destaque por likes decrescente e ativas
#         """
#         self.viagem2.likes.add(self.user)

#         response = self.client.get(self.url_home)
#         viagens_destaque = response.context['destaques']
#         self.assertEquals(viagens_destaque[0].titulo, 'Segunda viagem')
#         self.assertEquals(viagens_destaque.count(), 3)

#     def test_ultimas_viagens_home(self):
#         """ Testar exibição das últimas viagens """
#         response = self.client.get(self.url_home)
#         ultimas_viagens = response.context['ultimas_viagens']
#         self.assertEquals(ultimas_viagens.count(), 3)


# class PontoTuristicoTestCase(TestCase):
    
#     def setUp(self):
#         self.client = Client()
#         self.url_login = reverse(settings.LOGIN_URL)
#         self.user = User.objects.create_user(
#             email='teste@teste.com',
#             password='senha_secreta'
#         )

#         self.viagem = Viagem.objects.create(
#             titulo = 'Primeira viagem',
#             localidade = 'São Paulo, SP - Brasil',
#             foto = 'foto.jpg',
#             resumo = 'Um bom lugar para se visitar',
#             ativo = True,
#             avaliacao = 3,
#             user = self.user
#         )
#         self.ponto_turistico = PontoTuristico.objects.create(
#             titulo = 'Ponto turistico',
#             opiniao = 'São Paulo, SP - Brasil',
#             foto = 'foto.jpg',
#             viagem = self.viagem
#         )
#         small_gif = (
#             b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
#             b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
#             b'\x02\x4c\x01\x00\x3b'
#         )
#         self.foto = SimpleUploadedFile(
#             'small.gif', small_gif, content_type='image/gif'
#         )

#         self.url_pontos_turisticos = reverse('criar-ponto-turistico', kwargs={'id_viagem': self.viagem.id})

#     def tearDown(self):
#         self.user.delete()
#         Viagem.objects.all().delete()

#     def test_acesso_pontos_turisticos(self):
#         """ Teste de acesso a pontos turísticos """
#         response = self.client.get(self.url_pontos_turisticos)
#         self.assertRedirects(response, self.url_login + f"?next={self.url_pontos_turisticos}")
#         self.client.login(email=self.user.email, password='senha_secreta')
#         response = self.client.get(self.url_pontos_turisticos)
#         self.assertEquals(response.status_code, 200)
#         self.assertTemplateUsed(response, 'viagens/ponto_turistico/index.html')
#         pontos_turisticos = response.context['pontos_turisticos']
#         self.assertEquals(pontos_turisticos.count(), 1)

#     def test_cadastrar_ponto_turistico_ok(self):
#         """ Teste de cadastrar um ponto turístico """
#         self.client.login(email=self.user.email, password='senha_secreta')

#         data = {
#             'titulo': 'Ponto turístico',
#             'opiniao': 'Minha opinião do local',
#             'foto': self.foto
#         }
#         response = self.client.post(self.url_pontos_turisticos, data, format='multipart')
#         self.assertEquals(response.status_code, 302)
#         last_ponto_turistico = PontoTuristico.objects.filter(titulo='Ponto turístico').last()
#         self.assertRedirects(response, reverse('detalhes-ponto-turistico', kwargs={'pk': last_ponto_turistico.id}))

#     def test_cadastrar_ponto_turistico_error(self):
#         """ Teste de cadastrar um ponto turístico com falha """
#         self.client.login(email=self.user.email, password='senha_secreta')

#         data = {
#             'titulo': '',
#             'opiniao': '',
#             'foto': ''
#         }
#         response = self.client.post(self.url_pontos_turisticos, data, format='multipart')

#         self.assertFormError(response, 'form', 'titulo', 'Este campo é obrigatório.')
#         self.assertFormError(response, 'form', 'opiniao', 'Este campo é obrigatório.')
#         self.assertFormError(response, 'form', 'foto', 'Este campo é obrigatório.')

#     def test_atualizar_ponto_turistico_ok(self):
#         """ Teste de atualizar ponto turístico """
#         self.client.login(email=self.user.email, password='senha_secreta')
#         url_atualizar = reverse('atualizar-ponto-turistico', kwargs={'pk': self.ponto_turistico.id})

#         data = {
#             'titulo': 'Novo título do ponto turístico',
#             'opiniao': 'opinião atualizada',
#             'foto': self.foto
#         }
#         response = self.client.post(url_atualizar, data, format='multipart')
#         self.assertEquals(response.status_code, 302)
#         self.assertRedirects(response, reverse('detalhes-ponto-turistico', kwargs={'pk': self.ponto_turistico.id }))

#         self.ponto_turistico.refresh_from_db()
#         self.assertEquals(self.ponto_turistico.titulo, 'Novo título do ponto turístico')
#         self.assertEquals(self.ponto_turistico.opiniao, 'opinião atualizada')

#     def test_atualizar_ponto_turistico_error(self):
#         """ Teste de atualizar ponto turístico """
#         self.client.login(email=self.user.email, password='senha_secreta')
#         url_atualizar = reverse('atualizar-ponto-turistico', kwargs={'pk': self.ponto_turistico.id})

#         data = {
#             'titulo': '',
#             'opiniao': ''
#         }
#         response = self.client.post(url_atualizar, data, format='multipart')
#         self.assertFormError(response, 'form', 'titulo', 'Este campo é obrigatório.')
#         self.assertFormError(response, 'form', 'opiniao', 'Este campo é obrigatório.')

#     def test_deletar_ponto_turistico(self):
#         """ Teste deletar ponto turistico """
#         url_deletar_ponto_turistico = reverse('deletar-ponto-turistico', kwargs={'pk': self.ponto_turistico.id})
#         response = self.client.get(url_deletar_ponto_turistico)
#         self.assertRedirects(response, self.url_login + f"?next={url_deletar_ponto_turistico}")
#         self.client.login(email=self.user.email, password='senha_secreta')
#         response = self.client.post(url_deletar_ponto_turistico)
#         self.assertEquals(response.status_code, 200)
#         self.assertEquals(PontoTuristico.objects.count(), 0)


# class PostViagemTestCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.url_login = reverse(settings.LOGIN_URL)
#         self.user = User.objects.create_user(
#             email='user1@teste.com',
#             password='senha_secreta'
#         )

#         self.user2 = User.objects.create_user(
#             email='user2@teste.com',
#             password='senha_secreta'
#         )

#         self.viagem = Viagem.objects.create(
#             titulo = 'Primeira viagem',
#             localidade = 'São Paulo, SP - Brasil',
#             foto = 'foto.jpg',
#             resumo = 'Um bom lugar para se visitar',
#             ativo = True,
#             avaliacao = 3,
#             user = self.user
#         )

#         self.viagem.likes.add(self.user2)

#         self.ponto_turistico = PontoTuristico.objects.create(
#             titulo = 'Ponto turistico',
#             opiniao = 'São Paulo, SP - Brasil',
#             foto = 'foto.jpg',
#             viagem = self.viagem
#         )
#         self.url_post_viagem = reverse('post-viagem', kwargs={'pk': self.viagem.pk })

#     def test_post_viagem(self):
#         """ Teste visualizar post de viagem """
#         response = self.client.get(self.url_post_viagem)
#         self.assertEquals(response.status_code, 200)
#         self.assertTemplateUsed(response, 'viagens/post_viagem/index.html')
#         viagem = response.context['viagem']
#         self.assertEquals(viagem.titulo, 'Primeira viagem')
#         self.assertEquals(viagem.ponto_turistico_viagem.count(), 1)
#         self.assertEquals(viagem.ponto_turistico_viagem.count(), 1)
#         self.assertEquals(viagem.likes.count(), 1)

#     def test_curtir_post_viagem(self):
#         """ Teste curtir postagem """
#         url_like_post = reverse('like-post', kwargs={'pk': self.viagem.pk })
#         response = self.client.post(url_like_post)
#         self.assertRedirects(response, self.url_login + f"?next={url_like_post}")
#         self.client.login(email=self.user.email, password='senha_secreta')
#         response = self.client.post(url_like_post)
#         self.assertEquals(response.status_code, 200)
#         self.assertEquals(self.viagem.likes.count(), 2)

#     def test_criar_comentario_ok(self):
#         """ Teste criar comentário na postagem """
#         url_criar_comentario = reverse('criar-comentario-viagem', kwargs={'id_viagem': self.viagem.pk })
#         data = {
#             'comentario': 'Realmente um bom lugar'
#         }
#         self.client.login(email=self.user.email, password='senha_secreta')
#         response = self.client.post(url_criar_comentario, data)
#         last_comentario = Comentario.objects.filter(comentario='Realmente um bom lugar').last()
#         self.assertRedirects(response, reverse('detalhes-comentario', kwargs={'pk': last_comentario.id}))

#     def test_criar_comentario_error(self):
#         """ Teste criar comentário na postagem com erro"""
#         url_criar_comentario = reverse('criar-comentario-viagem', kwargs={'id_viagem': self.viagem.pk })
#         data = {
#             'comentario': ''
#         }
#         response = self.client.post(url_criar_comentario, data)
#         self.assertRedirects(response, self.url_login + f"?next={url_criar_comentario}")
#         self.client.login(email=self.user.email, password='senha_secreta')
#         response = self.client.post(url_criar_comentario, data)
#         self.assertContains(response, 'Algo deu errado ao enviar seu comentário, tente novamente!')
        
#     def test_deletar_comentario(self):
#         """ Teste criar comentário na postagem com erro"""
#         comentario = Comentario.objects.create(
#             comentario='Um comentário',
#             user = self.user,
#             viagem = self.viagem
#         )
#         url_deletar_comentario = reverse('deletar-comentario', kwargs={'pk': comentario.pk })

#         response = self.client.post(url_deletar_comentario)
#         self.assertRedirects(response, self.url_login + f"?next={url_deletar_comentario}")
#         self.client.login(email=self.user.email, password='senha_secreta')
#         response = self.client.post(url_deletar_comentario)
#         self.assertEquals(response.status_code, 200)
#         self.assertEquals(Comentario.objects.count(), 0)



class ListaViagensTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.url_lista_viagens = reverse('lista-viagens')
        self.user = User.objects.create_user(
            email='user@teste.com',
            password='senha_secreta'
        )

        self.viagem = Viagem.objects.create(
            titulo = 'Viagem a São Paulo',
            localidade = 'São Paulo, SP - Brasil',
            foto = 'foto.jpg',
            resumo = 'Um bom lugar para se visitar',
            ativo = True,
            avaliacao = 3,
            user = self.user
        )

        self.viagem.data_postado = timezone.datetime(
            2021, 10, 10, tzinfo=timezone.get_default_timezone()
        )
        self.viagem.save()

        self.viagem2 = Viagem.objects.create(
            titulo = 'Viagem a Santos',
            localidade = 'Santos, SP - Brasil',
            foto = 'foto.jpg',
            resumo = 'Um bom lugar para se visitar',
            ativo = True,
            avaliacao = 5,
            user = self.user
        )

        self.viagem2.data_postado = timezone.datetime(
            2021, 10, 9, tzinfo=timezone.get_default_timezone()
        )
        self.viagem2.save()

    def test_lista_viagens(self):
        """ Teste lista de viagens """
        response = self.client.get(self.url_lista_viagens)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'viagens/lista-viagens.html')
        viagens = response.context['viagens']
        self.assertEquals(viagens.count(),2)

    def test_lista_viagens_teste_filtro_titulo(self):
        """ Teste lista de viagens com filtro de titulo"""
        response = self.client.get(self.url_lista_viagens + '?titulo=São Paulo')
        self.assertEquals(response.status_code, 200)
        viagens = response.context['viagens']
        self.assertEquals(viagens.count(), 1)  

    def test_lista_viagens_teste_filtro_localidade(self):
        """ Teste lista de viagens com filtro de localidade"""
        response = self.client.get(self.url_lista_viagens + '?localidade=santos')
        self.assertEquals(response.status_code, 200)
        viagens = response.context['viagens']
        self.assertEquals(viagens[0].titulo, 'Viagem a Santos')  
        self.assertEquals(viagens.count(), 1)  

    def test_lista_viagens_teste_filtro_ordenacao(self):
        """ Teste lista de viagens com filtro de ordenacao"""
        response = self.client.get(self.url_lista_viagens + '?ordenacao=asc')
        self.assertEquals(response.status_code, 200)
        viagens = response.context['viagens']
        self.assertEquals(viagens[0].titulo, 'Viagem a São Paulo')
        self.assertEquals(viagens.count(), 2)

    def test_lista_viagens_teste_filtro_periodo(self):
        """ Teste lista de viagens com filtro entre periodo"""
        response = self.client.get(
            self.url_lista_viagens + '?data_postado_min=2021-10-09&data_postado_max=2021-10-09'
        )
        self.assertEquals(response.status_code, 200)
        viagens = response.context['viagens']
        self.assertEquals(viagens.count(), 1)
        viagens = response.context['viagens']
        self.assertEquals(viagens[0].titulo, 'Viagem a Santos')
