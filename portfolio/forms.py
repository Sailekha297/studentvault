
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from .models import Student

User = get_user_model()


class StudentAccountCreationForm(forms.Form):
    register_no = forms.CharField(max_length=30)
    username = forms.CharField(max_length=150)
    temporary_password = forms.CharField(
        widget=forms.PasswordInput,
        min_length=12
    )

    def clean_register_no(self):
        register_no = self.cleaned_data["register_no"]

        student = Student.objects.filter(
            register_no=register_no
        ).first()

        if not student:
            raise forms.ValidationError(
                "No student found with this register number."
            )

        if student.user_id:
            raise forms.ValidationError(
                "This student already has a login account."
            )

        return register_no

    def clean_username(self):
        username = self.cleaned_data["username"]

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "This username is already taken."
            )

        return username

    def clean_temporary_password(self):
        password = self.cleaned_data["temporary_password"]
        validate_password(password)
        return password
