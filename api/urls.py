from django.urls import path

from datalab import views
from api import views

urlpatterns = [
    # path('', views.DataSetsList.as_view()),
    path('files/', views.DataSetsList.as_view(), name='dataset'),
]

