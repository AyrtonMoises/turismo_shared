from django.shortcuts import render
from django.db.models import Count

from viagens.models import Viagem


def home(request):
    """ Página principal do site """
    viagens_em_destaque = Viagem.objects.filter(
        ativo=True
        ).annotate(count_likes=Count('likes')).order_by('-count_likes')[:3]
    ultimas_viagens = Viagem.objects.filter(ativo=True).order_by('-id')[:3]

    dados = {
        'destaques': viagens_em_destaque,
        'ultimas_viagens': ultimas_viagens
    }

    return render(request, 'home/index.html', dados)