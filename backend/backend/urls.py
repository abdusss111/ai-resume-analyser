from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rest_framework.routers import DefaultRouter
from email_app.views import CVViewSet
from jobs.views import JobPostViewSet, JobApplicationViewSet
 

router = DefaultRouter()
router.register(r'cvs', CVViewSet, basename='cv')
router.register(r'jobs', JobPostViewSet, basename='job')
router.register(r'applications', JobApplicationViewSet, basename='application')
 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt')),
]
