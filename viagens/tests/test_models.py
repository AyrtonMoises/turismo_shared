from django.test import TestCase
from django.contrib.auth import get_user_model


from viagens.models import Viagem, PontoTuristico, Comentario


User = get_user_model()

class ViagemTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='meuemail@email.com',
            first_name="Primeiro Nome",
            last_name="Sobrenome",
            password='minhasenhasecreta'
        )

        self.viagem = Viagem.objects.create(
            titulo = 'Uma viagem',
            localidade = 'São Paulo, SP - Brasil',
            data_postado = '2021-10-08',
            foto = 'foto_viagem.jpg',
            resumo = 'Um bom lugar para se visitar',
            ativo = True,
            avaliacao = 3,
            user = self.user
        )
        self.viagem.likes.add(self.user)

        self.ponto_turistico = PontoTuristico.objects.create(
            titulo = 'Ponto turístico 1',
            opiniao = 'Um ponto turístico interessante',
            foto = 'ponto_turistico.jpg',
            viagem = self.viagem
        )
        self.comentario = Comentario.objects.create(
            comentario = 'Meu comentário',
            user = self.user,
            viagem = self.viagem
        )

    def tearDown(self):
        Viagem.objects.all().delete()
        PontoTuristico.objects.all().delete()
        Comentario.objects.all().delete()
        User.objects.all().delete()

    def test_criar_viagem(self):
        """ Criar viagem """
        Viagem.objects.create(
            titulo = 'Uma viagem 2',
            localidade = 'Santos, SP - Brasil',
            data_postado = '2021-10-08',
            foto = 'foto_viagem2.jpg',
            resumo = 'Um bom lugar para se visitar no verão',
            ativo = True,
            avaliacao = 5,
            user = self.user
        )
        self.viagem.likes.add(self.user)
        self.assertEqual(Viagem.objects.count(), 2)

    def test_atualizar_viagem(self): 
        """ Atualizar uma viagem """  
        self.viagem.titulo = 'Uma viagem nova'
        self.viagem.localidade = 'Itapecerica, SP - Brasil'
        self.viagem.foto = 'foto_viagem2.jpg'
        self.viagem.resumo = 'Um bom lugar para se visitar no outono'
        self.viagem.ativo = False
        self.viagem.avaliacao = 3
        self.viagem.likes.remove(self.user)
        self.viagem.save()

        self.assertEqual(self.viagem.titulo, 'Uma viagem nova')
        self.assertEqual(self.viagem.localidade, 'Itapecerica, SP - Brasil')
        self.assertEqual(self.viagem.foto, 'foto_viagem2.jpg')
        self.assertEqual(self.viagem.resumo, 'Um bom lugar para se visitar no outono')
        self.assertEqual(self.viagem.ativo, False)
        self.assertEqual(self.viagem.avaliacao, 3)
        self.assertNotIn(self.user, self.viagem.likes.all())
        
    def test_deletar_viagem(self):
        """ Deletar uma viagem """
        self.viagem.delete()
        self.assertEqual(Viagem.objects.count(), 0)

    def test_criar_ponto_turistico(self):
        """ Criar ponto turistico """
        PontoTuristico.objects.create(
            titulo = 'Ponto turístico 1',
            opiniao = 'Um ponto turístico interessante',
            foto = 'ponto_turistico.jpg',
            viagem = self.viagem
        )
        self.assertEqual(PontoTuristico.objects.count(), 2)

    def test_atualizar_ponto_turistico(self): 
        """ Atualizar um ponto turistico """  
        self.ponto_turistico.titulo = 'Ponto turístico Novo'
        self.ponto_turistico.opiniao = 'Uma opinião nova'
        self.ponto_turistico.foto = 'ponto_turistico2.jpg'
        self.viagem.save()

        self.assertEqual(self.ponto_turistico.titulo, 'Ponto turístico Novo')
        self.assertEqual(self.ponto_turistico.opiniao, 'Uma opinião nova')
        self.assertEqual(self.ponto_turistico.foto, 'ponto_turistico2.jpg')
        
    def test_deletar_ponto_turistico(self):
        """ Deletar um ponto turistico """
        self.ponto_turistico.delete()
        self.assertEqual(PontoTuristico.objects.count(), 0)

    def test_criar_comentario(self):
        """ Criar comentario """
        Comentario.objects.create(
            comentario = 'Meu comentário',
            user = self.user,
            viagem = self.viagem
        )
        self.assertEqual(Comentario.objects.count(), 2)

    def test_deletar_comentario(self):
        """ Criar ponto turistico """
        self.comentario.delete()
        self.assertEqual(Comentario.objects.count(), 0)


