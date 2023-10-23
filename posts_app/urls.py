from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post-list'),

    path('post-create', views.post_create, name = 'post-create'),

    path('post-detail/<int:id>/', views.post_detail, name='post-detail'),

    path('post-update/<int:id>/', views.post_up, name='post-update'),

    path('post-delete/<int:id>/', views.post_delete, name='post-delete'),

    path('post/<int:post_id>/add_comment/', views.add_comment, name='add-comment'),

    path('perfil/', views.post_perfil, name='post-perfil'),

    path('pesquisar/', views.pesquisar_posts, name='pesquisar_posts'),

    path('registra-perfil', views.registro, name='registra-perfil'),

    path('login/', views.user_login, name='user-login'),

    path('logout/', views.user_logout, name='user-logout'),

    path('editar-perfil/', views.editar_perfil, name='editar-perfil'),

    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete-comment'),

    path('check-auth/', views.check_authentication, name='check-auth'),


]