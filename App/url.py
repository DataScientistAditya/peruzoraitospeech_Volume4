from django.urls import path
from . import views


urlpatterns=[
    path("Register", views.Register, name="Register"),
    path("Login", views.Login, name="Login"),
    path("CompareSentences", views.CompareSentences, name="CompareSentences"),
]