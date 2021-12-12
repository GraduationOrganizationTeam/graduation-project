from django.urls import path
from .views import AlunoList, DisciplinaList, AvaliacaoList, ComentarioList

urlpatterns = [
    path('alunos/', AlunoList.as_view()),
    path('disciplinas/', DisciplinaList.as_view()),
    path('avaliacoes/', AvaliacaoList.as_view()),
    path('comentario/', ComentarioList.as_view()),
]