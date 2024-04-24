from django.urls import path

from . import views


urlpatterns = [
    path("", views.rooms, name="rooms"),

    path('edit_photo/', views.edit_photo, name='edit_photo'),
    path('edit_nickname/', views.edit_nickname, name='edit_nickname'),

    path('users/<str:username>/', views.user_profile, name='user_profile'),

    path("create/", views.CreateRoom.as_view(), name="room_create"),
    path("<str:room_name>/", views.room, name="room"),
    path("<str:room_name>/delete/", views.DeleteRoom.as_view(), name='room_delete'),

    path('room/<int:room_id>/delete', views.delete_room, name='room_delete2'),

     path('room/<int:pk>/edit/', views.UpdateRoom.as_view(), name='room_update'),

    path('api/delete/<int:room_id>', views.delete_room2, name='delete_room'),

    #rest api операции
    #path('room/<str:room_id>/delete/', views.RoomViewSet.as_view({'delete': 'destroy'}), name='room-delete2'),
    #path('room/<str:room_id>/delete/', views.RoomViewSet.as_view({'delete': 'destroy'}), name='room-delete3'),

]