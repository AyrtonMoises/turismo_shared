from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotAllowed

from viagens.models import Comentario, Viagem
from viagens.forms import ViagemForm, ComentarioForm

from viagens.filters import ViagemFilter


class ViagemCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    """ Cadastro de viagem """
    template_name = 'viagens/cadastro/cadastro-viagem.html'
    form_class = ViagemForm
    success_url = reverse_lazy('minhas-viagens')
    success_message = "Viagem cadastrada com sucesso!"

    def form_valid(self, form):
        """ Vincula usuário a viagem """
        form.instance.user = self.request.user
        return super().form_valid(form)


class ViagemUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    """ Lista viagens cadastradas pelo usuário"""
    template_name = 'viagens/cadastro/cadastro-viagem.html'
    form_class = ViagemForm
    success_message = "Viagem atualizada com sucesso!"

    def get_queryset(self):
        """ Filtra viagens por usuário """
        return Viagem.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('editar-viagem', kwargs={'pk': self.kwargs['pk'] })


class ViagemDeleteView(LoginRequiredMixin, DeleteView):
    """ Deletar viagem """
    template_name = 'viagens/cadastro/deletar-viagem.html'
    success_url = reverse_lazy('minhas-viagens')
    success_message = "Viagem deletada com sucesso!"

    def get_queryset(self):
        """ Filtra viagens por usuário """
        return Viagem.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(ViagemDeleteView, self).delete(request, *args, **kwargs)


class MinhasViagensListView(LoginRequiredMixin, ListView):
    """ Lista viagens cadastradas pelo usuário """
    template_name = 'viagens/cadastro/minhas-viagens.html'
    context_object_name = 'viagens'
    paginate_by = 10

    def get_queryset(self):
        """ Filtra viagens por usuário """
        return Viagem.objects.filter(
            user=self.request.user
        ).order_by('-data_postado')


class ListaViagensListView(ListView):
    """ Lista viagens cadastradas pelo usuário """
    template_name = 'viagens/lista-viagens.html'
    context_object_name = 'viagens'
    paginate_by = 5
    queryset = Viagem.objects.filter(ativo=True).order_by('-id')

    def get_queryset(self):
        """ Filtra viagens ativas com filtro """
        qs = self.queryset
        viagens_filtradas = ViagemFilter(self.request.GET, queryset=qs)
        return viagens_filtradas.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            filter=ViagemFilter(self.request.GET, queryset=self.queryset)
        )
        return context

def viagem_post(request, pk):
    """ Post da viagem cadastrada """
    viagem = get_object_or_404(Viagem, pk=pk, ativo=True)
    form = ComentarioForm()
    dados = {
        'viagem': viagem,
        'form_comentario': form
    }
    return render(request, 'viagens/post_viagem/index.html', dados)

@login_required
def criar_comentario_viagem(request, id_viagem):
    """ Criar comentário no post de viagem """
    form = ComentarioForm(request.POST)
    viagem = get_object_or_404(Viagem, pk=id_viagem)

    if form.is_valid():
        comentario = form.save(commit=False)
        comentario.viagem = viagem
        comentario.user = request.user
        comentario.save()
        return redirect("detalhes-comentario", pk=comentario.pk)
    else:
        return render(request, 'viagens/post_viagem/mensagem-erro-comentario.html')

@login_required
def deletar_comentario(request, pk):
    """ Deletar comentario """
    comentario = get_object_or_404(Comentario, id=pk, user=request.user)

    if request.method == "POST":
        comentario.delete()
        return HttpResponse("")

    return HttpResponseNotAllowed(["POST",])

@login_required
def detalhes_comentario(request, pk):
    """ Exibe dados do comentário """
    comentario = get_object_or_404(Comentario, id=pk)
    dados = {
        "comentario": comentario
    }
    return render(request, "viagens/post_viagem/detalhes-comentario.html", dados)

@login_required
def like_post(request, pk):
    """ Adicionar/Remove like do post de viagem """
    viagem = get_object_or_404(Viagem, pk=pk)

    if not request.user in viagem.likes.all():
        viagem.likes.add(request.user)
    else:
        viagem.likes.remove(request.user)

    dados = {
        "viagem": viagem
    }
    return render(request, "viagens/post_viagem/like-post.html", dados)

