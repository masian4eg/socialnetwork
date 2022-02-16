from django.db import models
from django.contrib.auth.models import User
from .utils import get_random_code
from django.template.defaultfilters import slugify
from django.db.models import Q # сложные запросы


class ProfileManager(models.Manager):

    def get_all_profiles_to_invite(self, sender):
        profiles = Profile.objects.all().exclude(user=sender) # все профили кроме отправителя
        profile = Profile.objects.get(user=sender) # отправитель
        qs = Relationship.objects.filter(Q(sender=profile) | Q(receiver=profile)) # фильтр отправитель or получатель
        print(qs)

        accepted = ([])
        for rel in qs:
            if rel.status == 'accepted': # заносим в список accepted профили подтвержденных друзей
                accepted.add(rel.receiver)
                accepted.add(rel.sender)
        print(accepted)

        available = [profile for profile in profiles if profile not in accepted]
        # если профиля нет в общем списке профилей, то добавляем его в список available
        print(available)
        return available

    def get_all_profiles(self, me):
        profiles = Profile.objects.all().exclude(user=me) # все профили кроме себя
        return profiles


class Profile(models.Model):
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default='no bio...', max_length=300)
    email = models.EmailField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    avatar = models.ImageField(default='avatar.png', upload_to='avatars/')
    friends = models.ManyToManyField(User, blank=True, related_name='friends')
    slug = models.SlugField(unique=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = ProfileManager()

    def get_friends(self):
        return self.friends.all()

    def get_friends_no(self):
        return self.friends.all().count()

    def get_posts_no(self):
        return self.posts.all().count()
    '''считаем кол-во постов взяв related_name из приложения posts, модели Post, значение author'''

    def get_all_authors_posts(self):
        return self.posts.all()

    def get_likes_given_no(self):
        likes = self.like_set.all()
        total_liked = 0
        for item in likes:
            if item.value == 'Like':
                total_liked += 1
        return total_liked
    '''так как в приложении posts в модели Like у post нет значения related_name, то
     устанавливаем связь через like_set'''

    def get_likes_received_no(self):
        posts = self.posts.all()
        total_liked = 0
        for item in posts:
            total_liked += item.liked.all().count()
        return total_liked
    '''???6 why liked (not likes)'''

    def __str__(self):
        return f'{self.user.username}-{self.created.strftime("%d-%m-%Y")}' # создание объекта юзер

    def save(self, *args, **kwargs):
        ex = False # переменная определяющая совпадение URL юзера после генерации, по умолчанию False
        if self.first_name and self.last_name:
            to_slug = slugify(str(self.first_name) + ' ' + str(self.last_name)) # слаг имени и фамилии юзера
            ex = Profile.objects.filter(slug=to_slug).exists() # сравнение с уже имеющимися URL других юзеров
            while ex: # если есть совпадение
                to_slug = slugify(to_slug + ' ' + str(get_random_code())) #добавляем рандом
                ex = Profile.objects.filter(slug=to_slug).exists() # зацикливаем пока не будет совпадений
        else:
            to_slug = str(self.user) # иначе URL будет юзернейм
        self.slug = to_slug
        super().save(*args, **kwargs)


STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted')
)


class RelationshipManager(models.Manager):
    def invitations_received(self, receiver):
        qs = Relationship.objects.filter(receiver=receiver, status='send')
        return qs


class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = RelationshipManager()

    def __str__(self):
        return f'{self.sender}-{self.receiver}-{self.status}'
