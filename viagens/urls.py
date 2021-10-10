from django.urls import path

from viagens.views.viagem import deletar_comentario

from .views import (
    home, MinhasViagensListView, ViagemCreateView, ViagemUpdateView, 
    ViagemDeleteView, ListaViagensListView,
    criar_ponto_turistico, atualizar_ponto_turistico, 
    deletar_ponto_turistico, detalhes_ponto_turistico,
    criar_form_ponto_turistico, viagem_post, criar_comentario_viagem,
    detalhes_comentario, deletar_comentario, like_post
)


urlpatterns = [
    #página principal
    path('', home, name="home"),

    #viagem
    path('minhas-viagens/', MinhasViagensListView.as_view(), name="minhas-viagens"),
    path('viagens/novo/', ViagemCreateView.as_view(), name="cadastrar-viagem"),
    path('viagens/editar/<int:pk>/', ViagemUpdateView.as_view(), name="editar-viagem"),
    path('viagens/deletar/<int:pk>/', ViagemDeleteView.as_view(), name="deletar-viagem"),
    path('viagens/', ListaViagensListView.as_view(), name="lista-viagens"),
    path('viagens/<int:pk>/', viagem_post, name="post-viagem"),
    path('viagens/like/<int:pk>/', like_post, name="like-post"),

    #comentários
    path('viagens/comentar_viagem/<int:id_viagem>/', criar_comentario_viagem, name="criar-comentario-viagem"),
    path('viagens/comentario/<int:pk>/', detalhes_comentario, name="detalhes-comentario"),
    path('viagens/comentario/<int:pk>/deletar/', deletar_comentario, name="deletar-comentario"),

    #pontos turísticos
    path('pontos_turisticos/<int:id_viagem>/', criar_ponto_turistico, name='criar-ponto-turistico'),
    path('ponto_turistico/<int:pk>/editar/', atualizar_ponto_turistico, name="atualizar-ponto-turistico"),
    path('ponto_turistico/<int:pk>/deletar/', deletar_ponto_turistico, name="deletar-ponto-turistico"),
    path('ponto_turistico/<int:pk>/', detalhes_ponto_turistico, name="detalhes-ponto-turistico"),
    path('ponto_turistico_form/', criar_form_ponto_turistico, name="criar-form-ponto-turistico"),
]
