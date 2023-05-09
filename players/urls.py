from django.urls import path
from . import views

urlpatterns = [
    path('players/', views.players, name='players'),
    path('test/', views.tester, name='tester'),
    path('events/', views.events, name='events'),
    path('players/<slug:slug>', views.playerdetail, name='playerdetail'),
    path('events/<int:id>', views.eventdetail, name='eventdetail'),
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('confirm/', views.confirm, name='confirm'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>', views.blogpost, name='blogpost'),
]