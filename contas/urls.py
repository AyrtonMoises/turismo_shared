from django.urls import path

from .views import (
    login, logout, perfil,
    CadastroCreateView, AlterarSenhaView, RedefinirSenhaView,
    RedefinirSenhaConfirmarView
)


urlpatterns = [
    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),
    path('cadastro/', CadastroCreateView.as_view(), name="cadastro"),
    path('perfil/', perfil, name="perfil"),
    path('alterar_senha/', AlterarSenhaView.as_view(), name="alterar_senha"),
    path('redefinir_senha/', RedefinirSenhaView.as_view(), name='redefinir_senha'),
    path('confirmar_redefinir_senha/<uidb64>/<token>/',
        RedefinirSenhaConfirmarView.as_view(),
        name='confirmar_redefinir_senha'
    ),
]
