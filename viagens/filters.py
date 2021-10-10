from django.db.models import Q, Value, fields
from django.db.models.functions import Concat
from django import forms

import django_filters
from django_filters import widgets

from viagens.models import Viagem


class ViagemFilter(django_filters.FilterSet):
    ORDENACAO_CHOICES = (
        ('asc','Ascendente'),
        ('desc', 'Decrescente'),
    )

    titulo = django_filters.CharFilter(
        label= 'Título', field_name='titulo', lookup_expr='icontains'
    )
    localidade = django_filters.CharFilter(
        label= 'Localidade', field_name='localidade', lookup_expr='icontains'
    )
    user = django_filters.CharFilter(
        label= 'Viajante', method='filter_user_name'
    )
    data_postado = django_filters.DateFromToRangeFilter(
        label='Período',
        widget=widgets.RangeWidget(attrs={'type': 'date'})
    )
    
    ordenacao = django_filters.ChoiceFilter(
        label='Ordenação',
        choices = ORDENACAO_CHOICES,
        method='filter_order_created'
    )

    def filter_order_created(self, queryset, name, value):
        """ Ordenação de viagem por criação """
        expression = 'id' if value == 'asc' else '-id'
        return queryset.order_by(expression)

    def filter_user_name(self, queryset, name, value):
        """ Filtro por primeiro, último e nome completo """
        queryset = queryset.annotate(
            full_name=Concat('user__first_name', Value(' '), 'user__last_name')
        )
        return queryset.filter(
            Q(user__first_name__icontains=value) | 
            Q(user__last_name__icontains=value)  |
            Q(full_name__icontains=value)            
        )