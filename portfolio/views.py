from django.shortcuts import render,get_object_or_404
from .models import Student,Certificate
def home(request):
    students=Student.objects.all().order_by('name')
    return render(request,'portfolio/home.html',{'students':students})
def profile(request,pk):
    student=get_object_or_404(Student,pk=pk)
    return render(request,'portfolio/profile.html',{'student':student})
def verify(request,verification_id):
    cert=get_object_or_404(Certificate,verification_id=verification_id)
    return render(request,'portfolio/verify.html',{'certificate':cert})
