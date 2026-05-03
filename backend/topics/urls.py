from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import TopicViewSet, generate_course

router = DefaultRouter()
router.register(r'', TopicViewSet, basename='topic')

urlpatterns = router.urls + [
    path('<int:topic_id>/generate/', generate_course),
]
