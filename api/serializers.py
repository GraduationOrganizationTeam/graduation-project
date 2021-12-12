from rest_framework import serializers

from app.models import Aluno, Disciplina, Comentario, Avaliacao


class AlunoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Aluno
        fields = ['nome']

class ComentarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comentario
        fields = ['id']

class DisciplinaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Disciplina
        fields = ['id']

class AvaliacaoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Avaliacao
        fields = ['id']

