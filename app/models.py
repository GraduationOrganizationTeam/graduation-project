from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.fields.related import OneToOneField
from django.contrib.auth.models import Permission

class Departamento(models.Model):
    nome = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.nome


class Disciplina(models.Model):
    nome = models.CharField(max_length=255, unique = True)
    slug = models.SlugField(null=False, unique=True) # não queremos que usuarios normais possam alterar https://learndjango.com/tutorials/django-slug-tutorial
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=20, unique = True)
    semestre = models.IntegerField(blank = True, null =  True)
    descricao = models.TextField()
    creditos_aula = models.IntegerField(default=0)           # mudança do projeto, atualiza depois
    creditos_trabalho = models.IntegerField(default=0)       # mudança do projeto, atualiza depois

    class Meta:
        ordering = ('nome',)

    def __str__(self):
        return self.nome


class Avaliacao(models.Model):
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, # Talvez pensar melhor a respeito
    )

    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    data_de_criacao = models.DateTimeField(auto_now_add=True)
    nota_1 = models.IntegerField(validators=[MinValueValidator(limit_value=0), MaxValueValidator(limit_value=10)])
    nota_2 = models.IntegerField(validators=[MinValueValidator(limit_value=0), MaxValueValidator(limit_value=10)])
    nota_3 = models.IntegerField(validators=[MinValueValidator(limit_value=0), MaxValueValidator(limit_value=10)])
    nota_4 = models.IntegerField(validators=[MinValueValidator(limit_value=0), MaxValueValidator(limit_value=10)])

    class Meta:
        ordering = ['-data_de_criacao']

    def __str__(self):
        return f"avaliação feita por {self.autor} para {self.disciplina}"


class Comentario(models.Model):
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null = True,   # significa que pode ser vazio na nossa database
        blank = False  # mas não no preenchimento de formulários django
    )

    disciplina = models.ForeignKey(
        Disciplina,
        on_delete=models.CASCADE,    
    )

    comentario_pai = models.ForeignKey('self',
                                        on_delete=models.CASCADE,
                                        blank = True,
                                        null = True)
    excluido = models.BooleanField()
    conteudo = models.TextField()
    data_de_criacao = models.DateTimeField(auto_now_add=True)

    @property
    def get_total_likes(self):
        return self.likes.autor.count() - self.dislikes.autor.count()

    def __str__(self):
        return f"comentário feito por {self.autor} em {self.disciplina}"


class Like(models.Model):
    comentario = OneToOneField(Comentario, related_name="likes", on_delete=models.CASCADE)
    autor = models.ManyToManyField(settings.AUTH_USER_MODEL)
    
    def __str__(self):
        return f"likes dados em {self.comentario}"


class Dislike(models.Model):
    comentario = OneToOneField(Comentario, related_name="dislikes", on_delete=models.CASCADE)
    autor = models.ManyToManyField(settings.AUTH_USER_MODEL)
    
    def __str__(self):
        return f"dislikes dados em {self.comentario}"


class Aluno(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                primary_key=True)
    slug = models.SlugField(null=False, unique=True) # não queremos que usuarios normais possam alterar https://learndjango.com/tutorials/django-slug-tutorial
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    nome = models.CharField(max_length = 255)
    data_de_nascimento = models.DateField()
    file_path = models.CharField(max_length = 255, default="default.png") # alteração em relação ao projeto 
    ano_de_ingresso = models.IntegerField()
    disciplina = models.ManyToManyField(Disciplina)


class Professor(models.Model):
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    slug = models.SlugField(null=False, unique=True) # não queremos que usuarios normais possam alterar https://learndjango.com/tutorials/django-slug-tutorial
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                primary_key=True)
    nome = models.CharField(max_length = 255)
    data_de_nascimento = models.DateField()
    file_path = models.CharField(max_length = 255) # alteração em relação ao projeto 
    ano_de_ingresso = models.IntegerField()
    disciplina = models.ManyToManyField(Disciplina)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.usuario.has_perm('app.change_disciplina'):
            self.usuario.user_permissions.add(Permission.objects.filter(codename='change_disciplina')[0])

class Contato(models.Model):
    ASSUNTOS =(
    ("1", "Preciso de ajuda"),
    ("2", "Encontrei um bug no site"),
    ("3", "Encontrei um erro nos dados"),
    ("4", "Sou professor e não gostei de algo"),
    ("5", "Outro assunto"),
)
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    assunto = models.CharField(max_length=1,
                  choices=ASSUNTOS,
                  default="5")
    texto = models.TextField(max_length=1000)