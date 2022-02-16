from django.shortcuts import render
from .models import Profile, Relationship
from .forms import ProfileModelForm
from django.views.generic import ListView
from django.contrib.auth.models import User


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


def invites_received_view(request):
    profile = Profile.objects.get(user=request.user)
    qs = Relationship.objects.invitations_received(profile)

    context = {'qs': qs}

    return render(request, 'profiles/my_invites.html', context)


def invite_profiles_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles_to_invite(user)

    context = {'qs': qs}

    return render(request, 'profiles/to_invite_list.html', context)


def profiles_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles(user)

    context = {'qs': qs}

    return render(request, 'profiles/profile_list.html', context)


class ProfileListView(ListView):
    model = Profile
    template_name = 'profiles/profile_list.html'
    context_object_name = 'qs' # название qs уже используется в шаблоне

    def get_queryset(self):
        qs = Profile.objects.get_all_profiles(self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user) # iexact возвращает юзернейм без учета регистра знаков
        profile = Profile.objects.get(user=user) # получаем профиль юзера
        rel_r = Relationship.objects.filter(sender=profile) # список отправленных запросов на добавление в друзья
        rel_s = Relationship.objects.filter(receiver=profile) # список принятых запросов на добавление в друзья
        rel_receiver = []
        rel_sender = [] # пустые списки для добавления в них отправленных и принятых запросов в друзья

        for item in rel_r:
            rel_receiver.append(item.receiver.user)

        for item in rel_s:
            rel_sender.append(item.sender.user)

        context['rel_receiver'] = rel_receiver
        context['rel_sender'] = rel_sender

        context['is_empty'] = False
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True

        return context
