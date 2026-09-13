from django.urls import path
from rest_framework.routers import DefaultRouter
from .api import StudentViewSet,ProjectViewSet,CertificateViewSet
from . import views
router=DefaultRouter()
router.register('students',StudentViewSet); router.register('projects',ProjectViewSet); router.register('certificates',CertificateViewSet)
urlpatterns=[path('',views.home,name='home'),path('student/<int:pk>/',views.profile,name='profile'),path('verify/<str:verification_id>/',views.verify,name='verify'),path('api/',__import__('django').urls.include(router.urls))]
