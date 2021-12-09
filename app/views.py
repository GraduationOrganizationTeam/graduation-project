from .models import *
from django.db.models import Avg
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.views import generic
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.forms import ValidationError
from .models import Avaliacao, Aluno
from .forms import AvaliacaoForm
from datetime import datetime


class DisciplinaListView(generic.ListView):
    paginate_by = 10
    model = Disciplina
    template_name = 'list.html'
    context_object_name = 'lista_disciplinas'

    def get_queryset(self):
        queryset = Disciplina.objects.all()
        if self.request.GET.get("query", False):
            search_term = self.request.GET['query'].lower()
            queryset = queryset.filter(nome__icontains=search_term)
        return queryset        

class DisciplinaDetailView(generic.DetailView):
    model = Disciplina
    template_name = 'detail.html'

    def get_context_data(self, **kwargs):
        avals = Avaliacao.objects.filter(disciplina = self.object.id).aggregate(Avg("nota_1"),Avg("nota_2"),Avg("nota_3"),Avg("nota_4"))

        context = super().get_context_data(**kwargs)
        context["lista_de_comentarios"] = Comentario.objects.filter(disciplina=self.object.id).order_by('-data_de_criacao')
        context["avaliacoes"] = avals
        return context

class AlunoDetailView(generic.DetailView):
    model = Aluno
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        return context

def create_avaliacao(request,slug):
    if request.user.is_authenticated:
        if request.method == 'POST':
            avaliacao_form = AvaliacaoForm(request.POST)

            # checando se a ultima avaliação foi há menos de cinco meses
            query = Avaliacao.objects.filter(disciplina__slug=slug, autor=request.user).order_by("-data_de_criacao")
            if query.exists():
                date_format = "%H:%M:%S"
                month = 2629800
                print(query.values("data_de_criacao")[0])
                diff = datetime.utcnow() - query[0].data_de_criacao.replace(tzinfo=None)
                if diff.days < 5*30:
                    raise ValidationError(_('Deve-se esperar 5 meses entre avaliações'),
                                            code='invalid')
            
            if avaliacao_form.is_valid():
                disciplina = Disciplina.objects.get(slug=slug)
                avaliacao = Avaliacao(autor=request.user, disciplina=disciplina,
                                    **avaliacao_form.cleaned_data)
                avaliacao.save()

                return HttpResponseRedirect(
                    reverse('subject', args=(avaliacao.disciplina.slug, )))
        else:
            avaliacao_form = AvaliacaoForm()
    else:
        return HttpResponseRedirect(
            reverse('login')
        )        
    context = {'disciplina_slug':slug, 'avaliacao_form': avaliacao_form}
    return render(request, 'avaliacao.html', context)

def index(request):
    context = {}
    return render(request, 'index.html', context)

def about(request):
    context = {}
    return render(request, 'about.html', context)

def contato(request):
    context = {}
    return render(request, 'contato.html', context)