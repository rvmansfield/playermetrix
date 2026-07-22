from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('players/', views.players, name='players'),
    path('contact/', views.contact, name='contact'),
    path('evaluate/', views.evaluate, name='evaluate'),
    path('results/<int:metric_id>/', views.results, name='results'),
    path('history/', views.metrics_history, name='metrics_history'),
    path('add/<slug:player_id>/', views.add, name='add'),
    path('profile/', views.profile_list, name='profile_list'),
    path('profile/new/', views.profile_create, name='profile_create'),
    path('profile/<int:profile_id>/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<int:profile_id>/delete/', views.profile_delete, name='profile_delete'),
    path('playerevaluation/', views.playerevaluation, name='playerevaluation'),
    path('events/', views.events, name='events'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('player/<slug:player_id>/', views.profile_detail, name='profile_detail'),
    path('players/<slug:player_id>/', views.profile_detail, name='profile_detail'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
]
