from django.urls import path
from . import views

urlpatterns = [
    path('start/', views.start_lesson),
    path('<int:lesson_id>/answer/', views.submit_answer),
    path('<int:lesson_id>/complete/', views.complete_lesson),
]
