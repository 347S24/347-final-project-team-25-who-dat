from django.urls import path
from .views import homepage, game, my_courses
from .views import attendance_view, student_attendance_view, professor_attendance_dashboard, mark_attendance, view_attendance_by_status

app_name = "homepage"

urlpatterns = [
    path("", view=homepage, name="home"),
    path('game/', game, {'mode': 'study'}, name='game'),
    path('game/name/', game, {'mode': 'name'}, name='game_name'),
    path('game/photo/', game, {'mode': 'photo'}, name='game_photo'),
    path('my-courses/', my_courses, name='my-courses'),
    path('attendance/', attendance_view, name='attendance'),
    path('attendance/student/', student_attendance_view, name='student_attendance_view'),
    path('attendance/professor/', professor_attendance_dashboard, name='professor_attendance_dashboard'),
    path('attendance/mark/<int:course_id>/<str:date>/', mark_attendance, name='mark_attendance'),
    path('attendance/status/<int:course_id>/<str:date>/<str:status>/', view_attendance_by_status, name='view_attendance_by_status'),
]
