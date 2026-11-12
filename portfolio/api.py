
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import Student, Project, Certificate
from .serializers import (
    StudentSerializer,
    ProjectSerializer,
    CertificateSerializer,
    )


class StudentVaultPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return True

        is_staff_group = user.groups.filter(
            name="Organization Staff"
        ).exists()

        is_superuser = user.is_superuser

        if not (is_staff_group or is_superuser):
            return False

        if is_superuser:
            verified = (
                request.session.get("mfa_verified") is True
                and request.session.get("mfa_verified_user_id") == user.pk
            )
            if not verified:
                return False

        model = view.queryset.model

        permission_action = {
            "POST": "add",
            "PUT": "change",
            "PATCH": "change",
            "DELETE": "delete",
        }

        action = permission_action.get(request.method)

        if action:
            permission = f"{model._meta.app_label}.{action}_{model._meta.model_name}"
            return user.has_perm(permission)

        return False


class SecureModelViewSet(ModelViewSet):
    permission_classes = [StudentVaultPermission]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        is_staff_group = user.groups.filter(
            name="Organization Staff"
        ).exists()

        if is_staff_group or user.is_superuser:
            return queryset

        if queryset.model == Student:
            return queryset.filter(user=user)

        return queryset.filter(student__user=user)


class StudentViewSet(SecureModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class ProjectViewSet(SecureModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class CertificateViewSet(SecureModelViewSet):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
