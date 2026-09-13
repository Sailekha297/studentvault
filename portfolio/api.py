from rest_framework.viewsets import ModelViewSet
from .models import Student,Project,Certificate
from .serializers import StudentSerializer,ProjectSerializer,CertificateSerializer
class StudentViewSet(ModelViewSet): queryset=Student.objects.all(); serializer_class=StudentSerializer
class ProjectViewSet(ModelViewSet): queryset=Project.objects.all(); serializer_class=ProjectSerializer
class CertificateViewSet(ModelViewSet): queryset=Certificate.objects.all(); serializer_class=CertificateSerializer
