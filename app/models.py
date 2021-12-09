from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

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
    exlcuido = models.BooleanField()
    conteudo = models.TextField()
    data_de_criacao = models.DateTimeField(auto_now_add=True)
    curtidas = models.IntegerField()

    def __str__(self):
        return f"comentário feito por {self.autor} em {self.disciplina}"

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
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                primary_key=True)
    nome = models.CharField(max_length = 255)
    data_de_nascimento = models.DateField()
    file_path = models.CharField(max_length = 255) # alteração em relação ao projeto 
    ano_de_ingresso = models.IntegerField()
    disciplina = models.ManyToManyField(Disciplina)