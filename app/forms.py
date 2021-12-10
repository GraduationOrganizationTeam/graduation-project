from django import forms
from django.forms import ModelForm, Textarea
from django.forms import widgets
from django.forms.widgets import RadioSelect
from .models import Avaliacao, Comentario, Contato

class AvaliacaoForm(ModelForm):
   
    class Meta:
        model = Avaliacao
        fields = [
            'nota_1',
            'nota_2',
            'nota_3',
            'nota_4', 
        ]
        labels = {
            'nota_1': 'Ensino',
            'nota_2': 'Material Didático:',
            'nota_3': 'Avaliações:',
            'nota_4': 'Dificuldade:' 
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)

        CHOICES = [(i,str(i)) for i in range(1,11)]
        for field in self.fields:
            self.fields[field].widget = RadioSelect(choices=CHOICES)


class ComentarioForm(ModelForm):
    class Meta:
        model=Comentario
        fields=('conteudo',)
        labels={'conteudo':"Conteúdo"}

    def __init__(self, *args, **kwargs):
        super(ComentarioForm, self).__init__(*args, **kwargs)
        self.fields['conteudo'].widget.attrs["class"] = "comment-conteudo form-control"


class ContatoForm(ModelForm):
    class Meta:
        model = Contato
        fields = [
            'nome',
            'email',
            'assunto',
            'texto'
        ]
        labels = {
            'nome': 'Nome',
            'email': 'E-mail',
            'assunto': 'Assunto',
            'texto': 'Texto'
        }

    def __init__(self, *args, **kwargs):
        super(ContatoForm, self).__init__(*args, **kwargs)
        self.fields['nome'].widget.attrs["class"] = "contact-name"
        self.fields['email'].widget.attrs["class"] = "contact-email"
        self.fields['assunto'].widget.attrs["class"] = "contact-assunto"
        self.fields['texto'].widget.attrs["class"] = "contact-texto"