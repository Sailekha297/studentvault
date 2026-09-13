from django.core.management.base import BaseCommand
from portfolio.models import Student, Project, Certificate


class Command(BaseCommand):
    help = "Create demo StudentVault data"

    def handle(self, *args, **kwargs):

        student, created = Student.objects.get_or_create(
            register_no="24BCE1001",
            defaults={
                "name": "Ria Sharma",
                "department": "Computer Science",
                "email": "ria@example.com",
                "skills": "Python, Django, Cloud Computing",
            },
        )

        Project.objects.get_or_create(
            student=student,
            title="Cloud-Based Student Portfolio",
            defaults={
                "description": "A cloud application for managing student projects and certificates.",
                "technologies": "Django, REST API, PostgreSQL",
                "github_link": "https://github.com/example/student-portfolio",
            },
        )

        Project.objects.get_or_create(
            student=student,
            title="Private Security Browser",
            defaults={
                "description": "A website extension that allows the user to handle their own security requirements.",
                "technologies": "JavaScript, PostgreSQL, HTML",
                "github_link": "https://github.com/example/private-security-browser",
            },
        )

        Certificate.objects.get_or_create(
            verification_id="CERT-RIA-001",
            defaults={
                "student": student,
                "certificate_name": "Cloud Computing Fundamentals",
                "issuer": "Example Institute",
                "issue_date": "2026-08-15",
                "status": "Verified",
            },
        )

        Certificate.objects.get_or_create(
            verification_id="CERT-RIA-002",
            defaults={
                "student": student,
                "certificate_name": "Fundamentals in Python",
                "issuer": "Example Institute",
                "issue_date": "2026-06-03",
                "status": "Verified",
            },
        )

        self.stdout.write(
            self.style.SUCCESS("StudentVault demo data created successfully.")
        )