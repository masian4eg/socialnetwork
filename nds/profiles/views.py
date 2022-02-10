from django.shortcuts import render
from .models import Profile
from .forms import ProfileModelForm


def my_profile_view(request): # вьюха своего профиля
    profile = Profile.objects.get(user=request.user) # через гет запрос берем данные юзера
    form = ProfileModelForm(request.POST or None, request.FILES or None, instance=profile)
    # добавляем форму для обновления данных профиля, (показать данные профиля в форме)
    confirm = False # флаг подтверждения изменений

    if request.method == 'POST': # при обновлении данных, если все поля заполнены верно информация сохраняется
        if form.is_valid():
            form.save()
            confirm = True # с этим флагом в шаблоне выходит сообщение "обновлено"

    context = {
        'profile': profile,
        'form': form,
        'confirm': confirm,
    } # загоняем в контекст страницы данные из контекст словаря

    return render(request, 'profiles/myprofile.html', context) # рендерим на страницу личных данных профиля запрос и контекст
