from django.urls import path

from datalab import views

urlpatterns = [
    path('', views.dataset),
    path('file/', views.dataset, name='file'),
    path('profile/', views.profile, name='profile'),
    path('profile_config/', views.profile_config, name='profile_config'),
    path('experiment/', views.experiment, name='experiment'),
    path('delete_dataset/<int:pk>/', views.delete_dataset, name='delete_dataset'),
    path('delete_profile/<int:pk>/', views.delete_profile, name='delete_profile'),
    path('delete_experiment/<int:pk>/', views.delete_experiment, name='delete_experiment'),
    path('research/', views.research, name='research')

]
