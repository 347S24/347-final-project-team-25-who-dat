from django.urls import path

from .views import homepage, game, attendance, my_courses

app_name = "homepage"

urlpatterns = [
    path("", view=homepage, name="home"),
    path('attendance/', attendance, name='attendance'),
    # path('attendance/<int:course_id>/', attendance, name='attendance'),
    path('game/', game, {'mode': 'study'}, name='game'),
    path('game/name/', game, {'mode': 'name'}, name='game_name'),
    path('game/photo/', game, {'mode': 'photo'}, name='game_photo'),
    path('my-courses/', my_courses, name='my-courses'),
]
