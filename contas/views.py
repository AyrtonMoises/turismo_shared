from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth import get_user_model
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.views import (
    PasswordChangeView, PasswordResetView, PasswordResetConfirmView
)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required

from .forms import (
    UserForm, PerfilForm, AlterarSenhaForm, 
    RecuperarSenhaForm, UserPerfilForm
)


User = get_user_model()

def login(request):
    """ Caso esteja logado redireciona a home """
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('home')

    """ Realiza login do usuario """
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']

        if email == "" or senha == "":
            messages.error(request, "Campos email e senha não podem ficar em branco!")
            return redirect('login')
        user = auth.authenticate(request, username=email, password=senha)

        if user is not None:
            auth.login(request, user)
            proxima_pagina = request.POST.get('next')
            if proxima_pagina:
                return redirect(proxima_pagina)
            return redirect('home')
        else:
            messages.error(request, "Email/Senha estão incorretos")
            return render(request, 'contas/login.html')

    return render(request, 'contas/login.html')


def logout(request):
    """ Realiza logout do usuário """
    auth.logout(request)
    return redirect('home')


class CadastroCreateView(CreateView):
    """ Cadastro do usuário no sistema """
    form_class = UserForm
    model = User
    template_name = 'contas/cadastro.html'
    success_url = reverse_lazy('perfil')

    def form_valid(self, form):
        """ Autentica usuário após cadastro """
        valid = super().form_valid(form)
        user = auth.authenticate(
            email=self.request.POST['email'],
            password=self.request.POST['password1']
        )
        auth.login(self.request, user)
        return valid


@login_required
def perfil(request):
    """ Salva alterações de perfil e usuário """
    if request.method == 'POST':
        form_user = UserPerfilForm(request.POST, instance=request.user)
        form_perfil = PerfilForm(request.POST, request.FILES, instance=request.user.perfil)

        if form_user.is_valid() and form_perfil.is_valid():
            form_user.save()
            form_perfil.save()
            messages.success(request, 'Perfil atualizado com sucesso')
            return redirect('perfil')
    else:
        form_user = UserPerfilForm(instance=request.user)
        form_perfil = PerfilForm(instance=request.user.perfil)

    return render(request, 'contas/perfil.html', {'form_user': form_user, 'form_perfil': form_perfil})


class AlterarSenhaView(SuccessMessageMixin, PasswordChangeView):
    """ Alteração de senha """
    template_name = 'contas/alterar-senha.html'
    form_class = AlterarSenhaForm
    success_message = "Senha atualizada com sucesso!"
    success_url = reverse_lazy('home')


class RedefinirSenhaView(SuccessMessageMixin, PasswordResetView):
    """ Envia email de recuperação de senha """
    template_name = 'contas/redefinir-senha.html'
    form_class = RecuperarSenhaForm
    email_template_name = 'contas/template-redefinir-senha.html'
    subject_template_name = 'contas/assunto-redefinir-senha'
    success_message = "Um email foi enviado para sua caixa de entrada." \
                      "Verifique também sua caixa de spam antes de tentar novamente." 
    success_url = reverse_lazy('login')


class RedefinirSenhaConfirmarView(SuccessMessageMixin, PasswordResetConfirmView):
    """ Redefinir senha """
    template_name='contas/confirmar-redefinir-senha.html'
    success_url=reverse_lazy('login')
    success_message = "Senha alterada com sucesso!"

def home(request):
    """ Página principal do site """
    return render(request, 'home/index.html')