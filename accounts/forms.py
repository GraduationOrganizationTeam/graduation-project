from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from app.models import Departamento

class Signupform(UserCreationForm):

    email = forms.EmailField(max_length=200)
    nome = forms.CharField(max_length=255)
    ano_de_ingresso = forms.IntegerField()
    departamento = forms.ModelChoiceField(queryset=Departamento.objects, empty_label="Selecione seu departamento")
    data_de_nascimento = forms.DateField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:

            # esconde os textos de auxílio dentro do hover das tags
            help_text = self.fields[field].help_text
            self.fields[field].help_text = None
            if help_text != '':

                # formatação do texto de auxílio
                tags_to_remove = [("<li>",""),("</li>","\n"),("<ul>",""),("</ul>","")]
                for tag in tags_to_remove:
                    help_text = help_text.replace(tag[0],tag[1])

                self.fields[field].widget.attrs['title'] = help_text

            # aplica estilo do django para fields que não são de seleção
            if type(self.fields[field].widget)!=forms.widgets.Select:
                self.fields[field].widget.attrs["class"] = "form-control"
            # aplica estilo do django para fields que são de seleção
            else:
                self.fields[field].widget.attrs["class"] = "form-select"

    class Meta:
        model = User
        fields = ('nome', 'email', 'ano_de_ingresso', 'departamento', 'username', 'password1', 'password2')
