from django.contrib import admin
from django.urls import path
from homepage.views import homepage, attendance, game

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage, name='homepage'),
    path('attendance/', attendance, name='attendance'),
    path('game/', game, name='game'),
]