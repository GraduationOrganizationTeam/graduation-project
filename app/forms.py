from django import forms
from django.forms import ModelForm, Form
from django.forms.widgets import RadioSelect
from .models import Avaliacao, Comentario, Contato, Departamento

class FiltroForm(Form):
    TYPES_OF_ORDERING=[(1,'Departamento'),(2,'Nome'),(3,'Creditos Aula'),(4,'Creditos Trabalho'),
                       (5, 'Numero de Comentarios'),(6,'Numero de Avaliações'),(7,'Ensino'),
                       (8,'Material'),(9,'Avaliações'),(10,'Dificuldade')]

    ordenar_por = forms.ChoiceField(choices=TYPES_OF_ORDERING)

    departamento = forms.ModelChoiceField(queryset=Departamento.objects, empty_label="")
    
    credito_aula = forms.IntegerField()
    credito_aula.widget.attrs = {'min':'1','max':'10'}

    credito_trabalho = forms.IntegerField()
    credito_trabalho.widget.attrs = {'min':'1','max':'10'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


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