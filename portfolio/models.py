from django.conf import settings
from django.db import models
class Student(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="student_profile"
    )
    name = models.CharField(max_length=100)
    register_no = models.CharField(max_length=30, unique=True)
    department = models.CharField(max_length=100)
    email = models.EmailField()
    skills = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return f'{self.name} ({self.register_no})'
class Project(models.Model):
    student=models.ForeignKey(Student,on_delete=models.CASCADE,related_name='projects')
    title=models.CharField(max_length=150)
    description=models.TextField()
    technologies=models.CharField(max_length=300,blank=True)
    github_link=models.URLField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.title
class Certificate(models.Model):
    student=models.ForeignKey(Student,on_delete=models.CASCADE,related_name='certificates')
    certificate_name=models.CharField(max_length=150)
    issuer=models.CharField(max_length=150)
    issue_date=models.DateField()
    verification_id=models.CharField(max_length=50,unique=True)
    file=models.FileField(upload_to='certificates/',blank=True,null=True)
    status=models.CharField(max_length=20,default='Verified')
    def __str__(self): return self.certificate_name
class MFADevice(models.Model):
    user = models.OneToOneField(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='mfa_device'
    )
    encrypted_secret = models.TextField()
    enabled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'MFA for {self.user.username}'