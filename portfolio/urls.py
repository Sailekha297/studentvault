
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api import StudentViewSet, ProjectViewSet, CertificateViewSet
from . import views

router = DefaultRouter()

router.register("students", StudentViewSet)
router.register("projects", ProjectViewSet)
router.register("certificates", CertificateViewSet)

urlpatterns = [
    path("", views.home, name="home"),
    path("student/<int:pk>/", views.profile, name="profile"),
    path("verify/<str:verification_id>/", views.verify, name="verify"),

    path("mfa/setup/", views.mfa_setup, name="mfa_setup"),
    path("mfa/challenge/", views.mfa_challenge, name="mfa_challenge"),

    path("api/", include(router.urls)),

    path(
    "staff/create-student-account/",
    views.create_student_account,
    name="create_student_account"
    ),

    path("staff/login/", views.staff_login, name="staff_login"),
    path("staff/dashboard/", views.staff_dashboard, name="staff_dashboard"),
    path("staff/logout/", views.staff_logout, name="staff_logout"),

    path("student/login/", views.student_login, name="student_login"),
    path("student/dashboard/", views.student_dashboard, name="student_dashboard"),
    path("student/logout/", views.student_logout, name="student_logout"),
]
