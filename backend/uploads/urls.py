from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_upload),
    path('<int:upload_id>/', views.upload_status),
]
