from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required

from viagens.models import Viagem, PontoTuristico
from viagens.forms import PontoTuristicaForm


@login_required
def criar_ponto_turistico(request, id_viagem):
    """ Cria ponto turístico """
    viagem = get_object_or_404(Viagem, id=id_viagem, user=request.user)
    pontos_turisticos = PontoTuristico.objects.filter(
        viagem=viagem).order_by('-id')
    form = PontoTuristicaForm(request.POST or None, request.FILES or None)

    if request.method == "POST":
        if form.is_valid():
            ponto_turistico = form.save(commit=False)
            ponto_turistico.viagem = viagem
            ponto_turistico.save()
            return redirect("detalhes-ponto-turistico", pk=ponto_turistico.pk)
        else:
            return render(request, "viagens/ponto_turistico/form-ponto-turistico.html", context={
                "form": form
            })

    context = {
        "form": form,
        "viagem": viagem,
        "pontos_turisticos": pontos_turisticos
    }

    return render(request, "viagens/ponto_turistico/index.html", context)

@login_required
def atualizar_ponto_turistico(request, pk):
    """ Atualiza ponto turístico """
    ponto_turistico = get_object_or_404(PontoTuristico, id=pk, viagem__user=request.user)
    form = PontoTuristicaForm(request.POST or None, request.FILES or None, instance=ponto_turistico)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("detalhes-ponto-turistico", pk=ponto_turistico.id)
    context = {
        "form": form,
        "ponto_turistico": ponto_turistico
    }

    return render(request, "viagens/ponto_turistico/form-ponto-turistico.html", context)

@login_required
def deletar_ponto_turistico(request, pk):
    """ Deleta ponto turístico """
    ponto_turistico = get_object_or_404(PontoTuristico, id=pk, viagem__user=request.user)

    if request.method == "POST":
        ponto_turistico.delete()
        return HttpResponse("")

    return HttpResponseNotAllowed(["POST",])

@login_required
def detalhes_ponto_turistico(request, pk):
    """ Exibe dados do ponto turístico """
    ponto_turistico = get_object_or_404(PontoTuristico, id=pk, viagem__user=request.user)
    context = {
        "ponto_turistico": ponto_turistico
    }
    return render(request, "viagens/ponto_turistico/detail-ponto-turistico.html", context)

@login_required
def criar_form_ponto_turistico(request):
    """ Adiciona novo formulário """
    form = PontoTuristicaForm()
    context = {
        "form": form
    }
    return render(request, "viagens/ponto_turistico/form-ponto-turistico.html", context)