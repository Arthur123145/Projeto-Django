from django import forms
from .models import Comment
from .models import Post, Perfil
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):
    class Meta:
        model = Post #modelo
        fields = ['title', 'description', 'image'] #campos do modelo

        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['nome', 'bio', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False

class RegistroForm(UserCreationForm):
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'input-field'}))
    senha = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput(attrs={'class': 'input-field'}))
    confirmasenha = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput(attrs={'class': 'input-field'}))
    nome = forms.CharField(max_length=100, required=False, help_text='Seu nome para Perfil', widget=forms.TextInput(attrs={'class': 'input-field'}))
    bio = forms.CharField(max_length=500, required=False, widget=forms.Textarea(attrs={'class': 'input-field'}))
    image = forms.ImageField(required=False, help_text='Escolha uma imagem de perfil (opcional)')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'nome', 'bio', 'image')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            perfil = Perfil(user=user, image=self.cleaned_data['image'], bio=self.cleaned_data['bio'],nome=self.cleaned_data['nome'])
            perfil.save()
        return user



