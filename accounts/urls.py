from django.urls import path
from . import views
from django.contrib.auth import REDIRECT_FIELD_NAME, views as auth_views
from django.urls import reverse

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
]