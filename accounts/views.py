from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import Signupform
from app.models import Aluno, Professor
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.core.exceptions import ObjectDoesNotExist

def signup(request):
    if request.method == 'POST':
        form = Signupform(request.POST)
        if form.is_valid():

            nome = form.cleaned_data.get("nome")
            ano_de_ingresso = form.cleaned_data.get("ano_de_ingresso")
            departamento = form.cleaned_data.get("departamento")
            email = form.cleaned_data.get("email")
            data_de_nascimento = form.cleaned_data.get("data_de_nascimento")
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")

            user = User.objects.create_user(username, email, password)
            user.save()

            aluno = Aluno.objects.create(usuario=user, slug=username, departamento=departamento,
                                        nome=nome, data_de_nascimento=data_de_nascimento, file_path="default.png",
                                        ano_de_ingresso=ano_de_ingresso)
            aluno.save()
            login(request, user)
            return HttpResponseRedirect(reverse('myprofile'))
    else:
        form = Signupform()

    context = {'form': form}
    return render(request, 'accounts/signup.html', context)

@login_required
def get_my_profile(request):

    try:
        aluno = Aluno.objects.get(usuario=request.user)
        slug = aluno.slug
        dec = '_aluno'
    except ObjectDoesNotExist:
        slug = request.user.professor.slug
        dec = '_professor'

    return HttpResponseRedirect(reverse('profile'+dec, args=(slug, )))