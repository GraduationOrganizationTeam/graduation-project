from django.forms import ModelForm, Textarea
from django.forms import widgets
from django.forms.widgets import RadioSelect
from .models import Avaliacao, Comentario

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