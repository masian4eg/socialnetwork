from django import forms
from .models import Profile


class ProfileModelForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'bio', 'avatar')
# добавляем класс формы профиля, мета класс в котором
# определяем с какой моделью работаем и какие поля будут
# редактироваться