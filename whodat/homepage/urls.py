from django.urls import path

from .views import homepage
app_name = "homepage"
urlpatterns = [
    path("", view=homepage, name="home"),
]
