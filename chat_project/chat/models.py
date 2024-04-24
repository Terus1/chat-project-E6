from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)     # Пользователь
    picture = models.ImageField(upload_to=user_directory_path, null=True, blank=True)       # Аватарка

    def __str__(self) -> str:
        return f'{self.user.username}'


class Room(models.Model):
    name = models.CharField(max_length=64)      # Название комнаты 
    slug = models.SlugField(unique=True)        # Какой-то slug
    members = models.ManyToManyField(User, related_name='room_users', blank=True, default=None)     # Участники

    def get_absolute_url(self):
        return reverse('room', kwargs={'room_name': self.slug})

    def __str__(self):
        return f'{self.name}'
    
    
class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')       # Куда отправить смс
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')       # Кто отправил
    text = models.TextField()       # Текст сообщения
    date_added = models.DateTimeField(auto_now_add=True)        # Дата написания

    def __str__(self) -> str:
        return f'Message - {self.text} ( Chat - {self.room})'



