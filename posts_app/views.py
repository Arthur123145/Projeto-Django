from django.shortcuts import render,get_object_or_404,redirect
from posts_app.models import Post,Comment
from .forms import PostForm, CommentForm,RegistroForm,PerfilForm
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect,HttpResponseForbidden,JsonResponse
from .models import Post,Perfil,Comment
from posts_app.forms import PostForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate,get_user
from django.contrib.auth.decorators import permission_required, login_required
from django.db.models import Q







def post_list(request):
    template_name = 'lista-post.html'
    posts = Post.objects.all()
    context = {
        'posts' : posts
        }
    return render(request, template_name, context)

def post_create(request):
    if request.method == 'POST': # para metodo POST
        form = PostForm(request.POST, request.FILES) 
        if form.is_valid():# se for valido
            form = form.save(commit=False)
            form.save()#salva

            
            messages.success(request, 'O post foi criado com sucesso') # mensagem qualificativa
            return HttpResponseRedirect(reverse('post-list'))#coloquei para retornar
    form = PostForm() #senão carrega o formulario
    return render(request, 'post-form.html', {"form": form, "messages": messages.get_messages(request)}) #nesse template


def post_detail(request, id):
    template_name = 'post-detail.html' #template
    post = Post.objects.get(id=id) #Metodo Get
    comment_form = CommentForm()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()

            return redirect('post-detail', id=post.id)
    print(post)
    context = {
        'post' : post,
        'comment_form': comment_form,
        }
    return render(request, template_name, context) 



def post_up(request, id):
    post = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        form.save()

        messages.warning(request, 'O post foi atualizado')
        return HttpResponseRedirect(reverse('post-detail', args=[post.id]))
    return render(request,'post-form.html', {"form" : form, "messages": messages.get_messages(request)})

def post_delete(request, id):
    post = Post.objects.get(id=id)
    if request.method == 'POST':

        post.delete()
        messages.error(request, 'O post foi deletado com sucesso')
        return HttpResponseRedirect(reverse('post-list'))
    return render(request, 'post-delete.html')

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect('post-detail', id=post_id)
        else:
            form = CommentForm()
    
        return render(request, 'add_comment.html', {'form': form, 'post': post})



@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # Verifique se o usuário logado é o autor do comentário
    if request.user == comment.author:
        comment.delete()
        # Redirecione de volta à página do post
        return redirect('post-detail', id=comment.post.id)
    else:
        # Se o usuário não é o autor do comentário, retorne uma resposta HTTP 403 (proibido)
        return HttpResponseForbidden("Você não tem permissão para excluir este comentário.")



@login_required
def post_perfil(request):
    template_name = 'post_perfil.html'
    posts = Post.objects.all()
    # Adicione o código para obter o perfil do usuário logado
    try:
        perfil = Perfil.objects.get(user=request.user)
        # Se o perfil existe, passe as informações para o contexto
        context = {
            'posts': posts,
            'nome': perfil.nome,
            'bio': perfil.bio,
            'image_url': perfil.image.url,
        }
    except Perfil.DoesNotExist:
        # Se o perfil não existe, defina as variáveis de contexto como vazias
        context = {
            'posts': posts,
            'nome': '',
            'bio': '',
            'image_url': '',
        }
    return render(request, template_name, context)


def pesquisar_posts(request):
    template_name = 'pesquisar-posts.html'
    termo = request.GET.get('termo')

    # Realiza uma pesquisa no campo 'title' (título) e 'description' (descrição) dos posts
    posts = Post.objects.filter(
        Q(title__icontains=termo) | Q(description__icontains=termo)
    )

    context = {
        'posts': posts,
        'termo': termo,
    }

    return render(request, template_name, context)

#começar os perfil:

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Processar os campos de imagem e bio, se necessário
            image = form.cleaned_data.get('image')
            bio = form.cleaned_data.get('bio')
            perfil, created = Perfil.objects.get_or_create(user=user)
            perfil.image = image
            perfil.bio = bio
            perfil.save()
            return redirect('post-perfil')  # Redirecionar para a página de perfil após o registro bem-sucedido
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('post-perfil')
        else:
            # Handle authentication failure, e.g., display an error message
            pass
    return render(request, 'login.html')

def user_logout(request):
    # Realiza o logout
    logout(request)

    # Limpa as informações de perfil
    if request.user.is_authenticated:
        user_profile = request.user.profile
        user_profile.bio = 'Bem-vindo ao meu perfil'
        user_profile.image = 'profile_images/default.jpg'
        user_profile.save()

    return redirect('post-list')


@login_required
def editar_perfil(request):
    perfil, created = Perfil.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('post-perfil')
    else:
        form = PerfilForm(instance=perfil)

    # Adicione o perfil atual ao contexto para que as informações do perfil sejam exibidas no template
    context = {
        'form': form,
        'perfil': perfil,  # Adicione isso ao contexto
    }

    return render(request, 'editar_perfil.html', context)





def check_authentication(request):
    is_authenticated = request.user.is_authenticated
    return JsonResponse({'is_authenticated': is_authenticated})

