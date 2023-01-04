from django.urls import path
from . import views

urlpatterns = [
    path('players/', views.players, name='players'),
    path('test/', views.tester, name='tester'),
]