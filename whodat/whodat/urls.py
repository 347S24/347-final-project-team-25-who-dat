from django.contrib import admin
from django.urls import path
from whodat.homepage.views import homepage, attendance, game, my_courses

app_name = 'whodat'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage, name='homepage'),
    path('attendance/', attendance, name='attendance'),
    path('game/', game, {'mode': 'study'}, name='game'),
    path('game/name/', game, {'mode': 'name'}, name='game_name'),
    path('game/photo/', game, {'mode': 'photo'}, name='game_photo'),
    path('my-courses/', my_courses, name='my-courses'),
]