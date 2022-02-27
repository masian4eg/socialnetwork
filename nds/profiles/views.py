from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Relationship
from .forms import ProfileModelForm
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
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


@login_required
def invites_received_view(request): # вьюха списка полученных запрос в друзья
    profile = Profile.objects.get(user=request.user)
    qs = Relationship.objects.invitations_received(profile)
    result = list(map(lambda x: x.sender, qs)) # lambda функция для создания списка профилей, сделавших запрос на добвление в друзья
    is_empty = False
    if len(result) == 0:
        is_empty = True

    context = {
        'qs': result,
        'is_empty': is_empty,
    }  # список из профилей сделавших запрос на добавление в друзья (без указания получателя (себя)), если никого - is_empty

    return render(request, 'profiles/my_invites.html', context)


@login_required
def accept_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        if rel.status == 'send':
            rel.status = 'accepted'
            rel.save()
    return redirect('profiles:my-invites-view')


@login_required
def reject_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        rel.delete()
    return redirect('profiles:my-invites-view')


@login_required
def invite_profiles_list_view(request): # вьюха списка всех профилей доступных для дружбы
    user = request.user
    qs = Profile.objects.get_all_profiles_to_invite(user)

    context = {'qs': qs}

    return render(request, 'profiles/to_invite_list.html', context)


@login_required
def profiles_list_view(request): # вьюха всех профилей
    user = request.user
    qs = Profile.objects.get_all_profiles(user)

    context = {'qs': qs}

    return render(request, 'profiles/profile_list.html', context)


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'profiles/detail.html'

    def get_object(self, slug=None):
        slug = self.kwargs.get('slug')
        profile = Profile.objects.get(slug=slug)
        return profile

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
        context['posts'] = self.get_object().get_all_authors_posts()
        context['len_posts'] = True if len(self.get_object().get_all_authors_posts()) > 0 else False
        return context


class ProfileListView(LoginRequiredMixin, ListView): # список отправленных и присланных запрос на добавление в друзья
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


@login_required
def send_invitation(request): # метод отправляет запрос на добавление в друзья другим пользователям
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.create(sender=sender, receiver=receiver, status='send')

        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my-profile-view')


@login_required
def remove_from_friends(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.get(
            (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))
        )
        rel.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my-profile-view')
