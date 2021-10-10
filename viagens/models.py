from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

from django_resized import ResizedImageField


NOTAS = (
    (1, 'Péssimo'),
    (2, 'Ruim'),
    (3, 'Bom'),
    (4, 'Ótimo'),
    (5, 'Excelente'),
)

User = get_user_model()

class Viagem(models.Model):

    titulo = models.CharField('Título', max_length=150)
    localidade = models.CharField('Localidade', max_length=200)
    data_postado = models.DateTimeField('Data postado', auto_now_add=True)
    foto = ResizedImageField(size=[640, 360], quality=80, upload_to='viagens/')
    resumo = models.TextField('Resumo')
    ativo = models.BooleanField('Ativo', default=True)
    avaliacao = models.SmallIntegerField(choices=NOTAS)
    likes = models.ManyToManyField(User)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='viagens_usuario')

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse('editar-viagem', kwargs={'pk': self.pk })


class PontoTuristico(models.Model):
    titulo = models.CharField('Título', max_length=150)
    opiniao = models.TextField('Opinião')
    foto = ResizedImageField(size=[640, 360], quality=80, upload_to='pontos_turisticos/')
    viagem = models.ForeignKey(Viagem, on_delete=models.CASCADE, related_name='ponto_turistico_viagem')

    def __str__(self):
        return self.titulo


class Comentario(models.Model):
    comentario = models.TextField('Comentário')
    data_hora = models.DateTimeField(auto_now_add=True)
    viagem = models.ForeignKey(Viagem, on_delete=models.CASCADE, related_name='comentarios_viagem')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usuarios_comentario')


