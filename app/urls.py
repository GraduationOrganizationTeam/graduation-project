from . import views
from django.urls import path

urlpatterns = [
    path('', views.index , name="index"),
    path('search/', views.DisciplinaListView.as_view() , name='search'),
    path('subject/<slug:slug>/', views.DisciplinaDetailView.as_view() , name="subject"),
    path('subject/update/<slug:slug>/', views.DisciplinaUpdateView.as_view(), name='update'),
    path('subject/fav/<slug:slug>/', views.fav_disciplina, name='fav'),
    path('about/', views.about, name="about"),
    path('contato/', views.contato, name="contato"),
    path('avaliacao/<slug:slug>/', views.create_avaliacao , name='avaliacao'),
    path('profile/aluno/<slug:slug>/', views.AlunoDetailView.as_view(), name='profile_aluno'),
    path('profile/professor/<slug:slug>/', views.ProfessorDetailView.as_view(), name='profile_professor'),
    path('newcomment/like/<int:comment_id>/<str:type>/', views.UpdateLikes.as_view(), name='likeview'),
    path('newcomment/<slug:disciplina_slug>/<int:parent_id>/', views.CreateComentarioAninhado.as_view(), name='post_comment_a'),
    path('newcomment/<slug:disciplina_slug>/', views.CreateComentario.as_view(), name='post_comment'),
    
]