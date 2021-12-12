from rest_framework import generics

from app.models import Aluno, Disciplina, Comentario, Avaliacao
from .serializers import AlunoSerializer, DisciplinaSerializer, ComentarioSerializer, AvaliacaoSerializer


class AlunoList(generics.ListAPIView):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer

class DisciplinaList(generics.ListAPIView):
    queryset = Disciplina.objects.all()
    serializer_class = DisciplinaSerializer

class ComentarioList(generics.ListAPIView):
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer

class AvaliacaoList(generics.ListAPIView):
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer