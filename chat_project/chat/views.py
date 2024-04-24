from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import DeleteView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect, HttpResponse

from rest_framework.response import Response
from rest_framework import viewsets, generics
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.decorators import api_view

from .models import *
from .serializers import *
from .forms import CreateRoomForm, ProfilePictureForm



import logging




@api_view(['DELETE'])
def delete_room2(request, room_id):   
    room = Room.objects.get(id=room_id)
    room.delete()
    return HttpResponse('Комната удалилась')
#  return Response({'message': 'Комната успешно удалена.'})



# ======================================================= APIViews =======================================================

class RoomDeleteView(generics.DestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_field = 'room_id'
    permission_classes = (permissions.AllowAny, )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)    
        
        return Response(status=status.HTTP_204_NO_CONTENT)



class RoomListView(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class RoomDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

# ======================================================= Viewsets =======================================================
class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = (permissions.AllowAny, )


    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     if instance:
    #         instance.delete()
    #         return Response(status=HTTP_204_NO_CONTENT)
    #     return Response(status=HTTP_404_NOT_FOUND)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


# ========================================================== Views ===================================================== 


# Личный кабинет
def user_profile(request, username):        
    user = get_object_or_404(User, username=username)

    profile_query = Profile.objects.filter(user=user)
    if profile_query.exists():
        profile = profile_query.first()
        picture = profile.picture
    else:
        picture = None
    return render(request, 'user_profile.html', {'user': user, 'picture': picture})


# Комната
@login_required
def room(request, room_name):
    room = get_object_or_404(Room, slug=room_name)
    messages = Message.objects.filter(room=room).order_by('-date_added')[:25]
    
    online_users = room.members.all()
    logging.debug(f"online_users: {online_users}")

    return render(request, 'room.html', {'room': room, 'messages': messages, 'online_users': online_users})


# Комнаты
@login_required
def rooms(request):
    rooms = Room.objects.all()
    return render(request, 'rooms.html', {'rooms': rooms})


# Создать комнату
class CreateRoom(LoginRequiredMixin, CreateView):
    form_class = CreateRoomForm
    template_name = 'room_create.html'

#------------------------------------Попытки удаления комнаты--------------------------------------------------------
# Удалить комнату (class)
class DeleteRoom(LoginRequiredMixin, DeleteView):       
    model = Room
    template_name = 'room_delete.html'
    success_url = reverse_lazy('rooms')

    slug_url_kwarg = 'room_name'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = self.get_object()
        context['room'] = room
        print(room.slug)  # Здесь "value" - это атрибут объекта комнаты, который вы хотите вывести
        return context

    def get_success_url(self):
        return reverse_lazy('rooms')


# Удалить комнату (функция)
def delete_room(request, room_id):
    room = Room.objects.get(id=room_id)
    room.delete()
    return redirect('/')
#----------------------------------------------Конец--------------------------------------------------------


class UpdateRoom(LoginRequiredMixin, UpdateView):
    form_class = CreateRoomForm
    model = Room
    template_name = 'room_edit.html'
    success_url = reverse_lazy('rooms')

# Изменить имя
def edit_nickname(request):
    user = request.user

    if request.method == 'POST':
        new_nickname = request.POST.get('nickname')
        user.username = new_nickname
        user.save()

        return redirect(reverse('user_profile', args=[user.username]))
    else:
        return render(request, 'edit_nickname.html', {'user': user})
    

# Изменить аватарку    
def edit_photo(request):
    Profile = get_user_model().profile.related.related_model

    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect(reverse('user_profile', args=[request.user.username]))
    else:
        form = ProfilePictureForm(instance=profile)

    return render(request, 'edit_photo.html', {'form': form})


