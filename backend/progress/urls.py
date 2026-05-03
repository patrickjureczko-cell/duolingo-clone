from django.urls import path
from . import views

urlpatterns = [
    path('<str:session_id>/', views.session_progress),
    path('<str:session_id>/topic/<int:topic_id>/', views.topic_progress),
]
