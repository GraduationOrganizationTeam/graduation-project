from .models import *
from django.db.models import Avg, Count
from django.views import View
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import generic
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.forms import ValidationError
from .models import Avaliacao, Aluno, Comentario, Like, Dislike, Contato
from .forms import AvaliacaoForm, ComentarioForm, ContatoForm, FiltroForm
from datetime import datetime


class DisciplinaListView(generic.ListView):
    paginate_by = 10
    model = Disciplina
    template_name = 'list.html'
    context_object_name = 'lista_disciplinas'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        #Passando a query como contexto
        query = self.request.GET.get('query')
        context['searchq'] = query.replace("+"," ")

        #Passando o formulário de filtro como contexto
        form = FiltroForm()
        context["filtro"] = form
        return context

    def get_queryset(self):
        queryset = Disciplina.objects.annotate(c1=Count('comentario__id'),c2=Count('avaliacao__id'),
                                        a1=Avg('avaliacao__nota_1'),a2=Avg('avaliacao__nota_2'),
                                        a3=Avg('avaliacao__nota_3'),a4=Avg('avaliacao__nota_4'))
        if self.request.GET.get("query", False):
            search_term = self.request.GET['query'].lower()
            queryset = queryset.filter(nome__icontains=search_term)

        if self.request.GET.get("o",False):

            
            ORDERING_DICT = {
                "1":'departamento',
                "2":'nome',
                "3":'creditos_aula',
                "4":'creditos_trabalho',
                "5":'-c1',
                "6":'-c2',
                "7":'-a1',
                "8":'-a2',
                "9":'-a3',
                "10":'-a4'
            }

            order_by = self.request.GET['o']
            dept     = self.request.GET['d']
            credito_a = self.request.GET['ca']
            credito_t = self.request.GET['ct']

            kwargs = {"departamento_id":dept,
                      "creditos_aula": credito_a,
                      "creditos_trabalho": credito_t}
            
            for k,v in kwargs.items():
                if v != "":
                    queryset = queryset.filter(**{k:v})
            queryset = queryset.order_by(ORDERING_DICT[order_by])

        return queryset        

class DisciplinaDetailView(generic.DetailView):
    model = Disciplina
    template_name = 'detail.html'

    def get_context_data(self, **kwargs):
        avals = Avaliacao.objects.filter(disciplina = self.object.id).aggregate(Avg("nota_1"),Avg("nota_2"),Avg("nota_3"),Avg("nota_4"))

        context = super().get_context_data(**kwargs)
        context["lista_de_comentarios"] = Comentario.objects.filter(disciplina=self.object.id).filter(comentario_pai=None).order_by('-data_de_criacao')
        context["avaliacoes"] = avals
        context["comentario_form"] = ComentarioForm()
        return context

class DisciplinaUpdateView(PermissionRequiredMixin, generic.UpdateView):
    model = Disciplina
    fields = ['descricao']
    template_name = 'update.html'
    permission_required = 'app.change_disciplina'


class AlunoDetailView(generic.DetailView):
    model = Aluno
    template_name = 'profile.html'
    context_object_name = 'conta'


class ProfessorDetailView(generic.DetailView):
    model = Professor
    template_name = 'profile.html'
    context_object_name = 'conta'
    

# Criar Comentário Aninhado
class CreateComentarioAninhado(LoginRequiredMixin, View):
    form_class = ComentarioForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        parent_id = self.kwargs.get("parent_id", None)
        disciplina_slug = self.kwargs.get("disciplina_slug", None)
        disciplina = get_object_or_404(Disciplina, slug=disciplina_slug)

        # se o pai tiver pai, retornar
        if parent_id != None:
            parent_comment = get_object_or_404(Comentario, id=parent_id)
            if parent_comment.comentario_pai is not None:
                return HttpResponseRedirect(reverse('subject', args=(disciplina_slug,)))
        else:
            parent_comment = None
        
        if form.is_valid():
            conteudo = form.cleaned_data["conteudo"]
            comentario = Comentario(autor=request.user, disciplina=disciplina,
                                    comentario_pai=parent_comment, excluido=False,
                                    conteudo=conteudo)
            comentario.save()
            return HttpResponseRedirect(reverse('subject', args=(disciplina_slug,)) + f"#{comentario.id}")


class CreateComentario(CreateComentarioAninhado):

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
        

class UpdateLikes(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):

        comment_id = self.kwargs.get('comment_id', None)
        type = self.kwargs.get('type', None)
        comment = get_object_or_404(Comentario, id=comment_id)

        Like.objects.get_or_create(comentario=comment)
        Dislike.objects.get_or_create(comentario=comment)

        if type.lower() == 'like':

            if request.user in comment.likes.autor.all():
                comment.likes.autor.remove(request.user)
            else:
                comment.likes.autor.add(request.user)
                comment.dislikes.autor.remove(request.user)
        elif type.lower() == 'dislike':

            if request.user in comment.dislikes.autor.all():
                comment.dislikes.autor.remove(request.user)
            else:
                comment.dislikes.autor.add(request.user)
                comment.likes.autor.remove(request.user)
        else:
            return HttpResponseRedirect(reverse('subject', args=(comment.disciplina.slug,))+ f"#{comment.id}")
        return HttpResponseRedirect(reverse('subject', args=(comment.disciplina.slug,))+ f"#{comment.id}")


@login_required
def create_avaliacao(request,slug):
    if request.method == 'POST':
        avaliacao_form = AvaliacaoForm(request.POST)

        # checando se a ultima avaliação foi há menos de cinco meses
        query = Avaliacao.objects.filter(disciplina__slug=slug, autor=request.user).order_by("-data_de_criacao")
        if query.exists():
            date_format = "%H:%M:%S"
            month = 2629800
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
                reverse('subject', args=(avaliacao.disciplina.slug,)))
    else:
        avaliacao_form = AvaliacaoForm()

    context = {'disciplina_slug':slug, 'avaliacao_form': avaliacao_form}
    return render(request, 'avaliacao.html', context)

def index(request):
    context = {}
    return render(request, 'index.html', context)

def about(request):
    context = {}
    return render(request, 'about.html', context)

def contato(request):
    if request.method == 'POST':
        contato_nome = request.POST['nome']
        contato_email = request.POST['email']
        contato_assunto = request.POST['assunto']
        contato_texto = request.POST['texto']
        contato = Contato(nome=contato_nome, email=contato_email, assunto=contato_assunto, texto=contato_texto)
        contato.save()
        return HttpResponseRedirect(
            reverse('contato'))
    else:
        form = ContatoForm()
        context = {'form': form}
        return render(request, 'contato.html', context)