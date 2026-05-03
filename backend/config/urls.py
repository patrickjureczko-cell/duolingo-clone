from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/topics/', include('topics.urls')),
    path('api/courses/', include('courses.urls')),
    path('api/lessons/', include('lessons.urls')),
    path('api/progress/', include('progress.urls')),
    path('api/uploads/', include('uploads.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
