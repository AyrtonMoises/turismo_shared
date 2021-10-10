from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm, PasswordResetForm

from .models import Perfil


User = get_user_model()

class UserForm(UserCreationForm):
    first_name = forms.CharField(
        label='Primeiro nome',
        max_length=150, 
        required=True, 
        widget=forms.TextInput(attrs={'class': "form-control"})
    )
    last_name = forms.CharField(
        label='Sobrenome',
        max_length=150, 
        required=True, 
        widget=forms.TextInput(attrs={'class': "form-control"})
    )
    email = forms.EmailField(
        label='Email',
        max_length=100, 
        required=True, 
        widget=forms.TextInput(attrs={'class': "form-control"})
    )
    password1 = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'class': "form-control"}),
        required=True,
        help_text="""Sua senha precisa conter pelo menos 8 caracteres<br>
            Sua senha não pode ser uma senha comumente utilizada<br>
            Sua senha não pode ser inteiramente numérica"""
    )
    password2 = forms.CharField(
        label='Confirme sua senha',
        widget=forms.PasswordInput(attrs={'class': "form-control"}),
        required=True
    )

    class Meta:
        model = User
        fields = ['first_name','last_name','email','password1','password2',]


class UserPerfilForm(forms.ModelForm):
    email = forms.CharField(
        label='Email',
        max_length=150, 
        required=True, 
        widget=forms.TextInput(attrs={'class': "form-control"})
    )
    first_name = forms.CharField(
        label='Primeiro nome',
        max_length=150, 
        required=True, 
        widget=forms.TextInput(attrs={'class': "form-control"})
    )
    last_name = forms.CharField(
        label='Sobrenome',
        max_length=150, 
        required=True, 
        widget=forms.TextInput(attrs={'class': "form-control"})
    )
    class Meta:
        model = User
        fields = ['first_name','last_name','email',]


class PerfilForm(forms.ModelForm):
    biografia = forms.CharField(
        label='Biografia',
        required=False, 
        widget=forms.Textarea(attrs={
            'class': "form-control",
            'rows': '4',
        })
    )
    foto = forms.FileField(
        label='Enviar foto',
        required=False,
        widget=forms.FileInput(attrs={'class': "form-control"})
    )
    facebook = forms.URLField(
        label='Facebook',
        required=False,
        widget=forms.URLInput(attrs={'class': "form-control"})
    )
    instagram = forms.URLField(
        label='Instagram',
        required=False,
        widget=forms.URLInput(attrs={'class': "form-control"})
    )
    twitter = forms.URLField(
        label='Twitter',
        required=False,
        widget=forms.URLInput(attrs={'class': "form-control"})
    )
    blog = forms.URLField(
        label='Blog pessoal',
        required=False,
        widget=forms.URLInput(attrs={'class': "form-control"})
    )

    field_order = ['foto',]

    class Meta:
        model = Perfil
        exclude = ['user',]


class AlterarSenhaForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Senha atual',
        required=True, 
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    new_password1 = forms.CharField(
        label='Nova Senha',
        required=True, 
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="""Sua senha precisa conter pelo menos 8 caracteres<br>
            Sua senha não pode ser uma senha comumente utilizada<br>
            Sua senha não pode ser inteiramente numérica"""
    )
    new_password2 = forms.CharField(
        required=True, 
        label='Confirmar senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text='Digite novamente a nova senha'
    )


class RecuperarSenhaForm(PasswordResetForm):
    email = forms.EmailField(
        label='Email',
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        help_text='Um email será enviado para sua caixa de entrada'
    )

    def clean_email(self):
        """ Valida email """
        email = self.cleaned_data.get('email')

        email_usuario = User.objects.filter(email=email)
        if not email_usuario:
            raise forms.ValidationError("Não existe um usuário com esse email")
        return email
