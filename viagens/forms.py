from django import forms

from .models import Comentario, Viagem, PontoTuristico, NOTAS


class ViagemForm(forms.ModelForm):
    titulo = forms.CharField(
        label='Título',
        max_length=150, 
        required=True, 
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'placeholder': 'Ex. Minha viagem a Argentina',
        })
    )
    localidade = forms.CharField(
        label='Localidade',
        max_length=200, 
        required=True, 
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'placeholder': 'Ex. El Calafate, Patagônia - Argentina'
        })
    )
    resumo = forms.CharField(
        label='Resumo da viagem',
        required=True, 
        widget=forms.Textarea(attrs={
            'class': "form-control",
            'rows': '4',
            'placeholder': 'Um breve resumo da sua viagem'
        })
    )
    avaliacao = forms.ChoiceField(
        label='Avaliação',
        choices=NOTAS,
        widget=forms.Select(attrs={
            'class': "form-control"
        }),
        initial=0
    )
    foto = forms.FileField(
        label='Enviar foto',
        required=True,
        widget=forms.FileInput(attrs={'class': "form-control"})
    )
    ativo = forms.BooleanField(
        label='Ativo',
        required=False,
        widget=forms.CheckboxInput(
           attrs={
               'class': 'form-check-input'
           }
        ),
        initial=True
    )

    field_order = ['titulo', 'localidade', 'resumo', 'avaliacao', 'foto', 'ativo',]

    class Meta:
        model = Viagem
        exclude = ['user','data_postado','likes',]


class PontoTuristicaForm(forms.ModelForm):
    titulo = forms.CharField(
        label='Título',
        max_length=150, 
        required=True, 
        widget=forms.TextInput(attrs={'class': "form-control"})
    )
    opiniao = forms.CharField(
        label='Opinião',
        required=True, 
        widget=forms.Textarea(attrs={
            'class': "form-control",
            'rows': '4',
            'placeholder': 'Um breve resumo do local visitado'
        })
    )
    foto = forms.FileField(
        label='Enviar foto',
        required=True,
        widget=forms.FileInput(attrs={'class': "form-control"})
    )
    
    class Meta:
        model = PontoTuristico
        exclude = ['viagem',]


class ComentarioForm(forms.ModelForm):
    comentario = forms.CharField(
        label='Envie um comentário',
        required=True, 
        widget=forms.Textarea(attrs={
            'class': "form-control",
            'rows': '2',
            'placeholder': 'Deixe aqui seu comentário'
        })
    )  
    class Meta:
        model = Comentario
        exclude = ['data_hora', 'viagem', 'user']