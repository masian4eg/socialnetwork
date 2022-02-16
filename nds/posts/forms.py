from django import forms
from .models import Post, Comment


class PostModelForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 2})) # размер текстовой формы дял поста

    class Meta: # поля из модели пост - контент и изображение
        model = Post
        fields = ('content', 'image')


class CommentModelForm(forms.ModelForm):
    body = forms.CharField(label='Комментарии', widget=forms.TextInput(attrs={'placeholder': 'Напишите коммент...'}))

    class Meta: # поля из модели коммент - текст комментария body
        model = Comment
        fields = ('body',)
