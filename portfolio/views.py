from django.core.exceptions import PermissionDenied
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db import transaction
from django.urls import reverse
from .forms import StudentAccountCreationForm
import base64
import io

import pyotp
import qrcode

from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.shortcuts import redirect
from django.urls import reverse

from .models import MFADevice
from .mfa_utils import encrypt_secret, decrypt_secret
from django.shortcuts import render,get_object_or_404
from .models import Student,Certificate

def home(request):
    return render(request, "portfolio/home.html")


@login_required(login_url="/student/login/")
def profile(request, pk):
    student = get_object_or_404(Student, pk=pk)

    is_staff = (
        request.user.groups.filter(name="Organization Staff").exists()
        or request.user.is_superuser
    )

    if not is_staff and student.user_id != request.user.id:
        raise PermissionDenied

    return render(
        request,
        "portfolio/profile.html",
        {"student": student}
    )


@login_required(login_url="/student/login/")
def verify(request, verification_id):
    certificate = get_object_or_404(
        Certificate,
        verification_id=verification_id
    )

    is_staff = (
        request.user.groups.filter(name="Organization Staff").exists()
        or request.user.is_superuser
    )

    if not is_staff and certificate.student.user_id != request.user.id:
        raise PermissionDenied

    return render(
        request,
        "portfolio/verify.html",
        {"certificate": certificate}
    )

User = get_user_model()


def get_mfa_user(request):
    if request.user.is_authenticated and request.user.is_staff:
        return request.user

    user_id = request.session.get("mfa_pending_user_id")

    if user_id:
        return User.objects.filter(
            pk=user_id,
            is_staff=True
        ).first()

    return None


def mfa_setup(request):
    user = get_mfa_user(request)

    if not user:
        return redirect("/admin/login/")

    device, created = MFADevice.objects.get_or_create(
        user=user,
        defaults={
            "encrypted_secret": encrypt_secret(
                pyotp.random_base32()
            )
        }
    )

    if device.enabled:
        return redirect("mfa_challenge")

    secret = decrypt_secret(device.encrypted_secret)

    if request.method == "POST":
        token = request.POST.get("token", "").strip().replace(" ", "")

        if pyotp.TOTP(secret).verify(token, valid_window=1):
            device.enabled = True
            device.save(update_fields=["enabled"])

            if not request.user.is_authenticated:
                login(request, user)

            request.session["mfa_verified"] = True
            request.session["mfa_verified_user_id"] = user.pk
            request.session.pop("mfa_pending_user_id", None)

            messages.success(request, "MFA enabled successfully.")
            return redirect("/admin/")

        messages.error(request, "Invalid authenticator code.")

    provisioning_uri = pyotp.TOTP(secret).provisioning_uri(
        name=user.username,
        issuer_name="StudentVault"
    )

    qr = qrcode.make(provisioning_uri)
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")

    qr_image = base64.b64encode(
        buffer.getvalue()
    ).decode()

    return render(
        request,
        "portfolio/mfa_setup.html",
        {"qr_image": qr_image}
    )


def mfa_challenge(request):
    user = get_mfa_user(request)

    if not user:
        return redirect("/admin/login/")

    device = MFADevice.objects.filter(
        user=user,
        enabled=True
    ).first()

    if not device:
        return redirect("mfa_setup")

    if request.method == "POST":
        token = request.POST.get("token", "").strip().replace(" ", "")

        secret = decrypt_secret(device.encrypted_secret)

        if pyotp.TOTP(secret).verify(token, valid_window=1):
            if not request.user.is_authenticated:
                login(request, user)

            request.session["mfa_verified"] = True
            request.session["mfa_verified_user_id"] = user.pk
            request.session.pop("mfa_pending_user_id", None)

            return redirect("/admin/")

        messages.error(request, "Invalid authenticator code.")

    return render(request, "portfolio/mfa_challenge.html")

@login_required(login_url="/staff/login/")
@user_passes_test(
    lambda user: user.groups.filter(name="Organization Staff").exists()
    or user.is_superuser,
    login_url="/staff/login/"
)
def create_student_account(request):

    if request.user.is_superuser:
        verified = (
            request.session.get("mfa_verified") is True
            and request.session.get("mfa_verified_user_id") == request.user.pk
        )

        mfa_enabled = MFADevice.objects.filter(
            user=request.user,
            enabled=True
        ).exists()

        if not mfa_enabled:
            return redirect("mfa_setup")

        if not verified:
            return redirect("mfa_challenge")

    if not (
        request.user.is_superuser
        or request.user.has_perm("portfolio.add_student")
    ):
        raise PermissionDenied

    if request.method == "POST":
        form = StudentAccountCreationForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                student = Student.objects.select_for_update().get(
                    register_no=form.cleaned_data["register_no"]
                )

                if student.user_id:
                    form.add_error(
                        "register_no",
                        "This student already has an account."
                    )
                else:
                    user = User.objects.create_user(
                        username=form.cleaned_data["username"],
                        password=form.cleaned_data["temporary_password"],
                        email=student.email
                    )

                    student.user = user
                    student.save(update_fields=["user"])

                    messages.success(
                        request,
                        f"Login account created for {student.name}."
                    )

                    return redirect("staff_dashboard")

    else:
        form = StudentAccountCreationForm()

    return render(
        request,
        "portfolio/create_student_account.html",
        {"form": form}
    )

def staff_login(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name="Organization Staff").exists():
            return redirect("staff_dashboard")

    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()

        if user.groups.filter(name="Organization Staff").exists():
            login(request, user)
            return redirect("staff_dashboard")

        form.add_error(None, "You do not have organization staff access.")

    return render(request, "portfolio/staff_login.html", {"form": form})


@login_required(login_url="/staff/login/")
@user_passes_test(
    lambda user: user.groups.filter(name="Organization Staff").exists(),
    login_url="/staff/login/"
)
def staff_dashboard(request):
    return render(request, "portfolio/staff_dashboard.html")


@login_required(login_url="/staff/login/")
def staff_logout(request):
    if request.method == "POST":
        logout(request)
        return redirect("staff_login")

    return redirect("staff_dashboard")

def student_login(request):
    if request.user.is_authenticated:
        if hasattr(request.user, "student_profile"):
            return redirect("student_dashboard")

    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()

        if hasattr(user, "student_profile"):
            login(request, user)
            return redirect("student_dashboard")

        form.add_error(None, "No student account is associated with these credentials.")

    return render(request, "portfolio/student_login.html", {"form": form})


@login_required(login_url="/student/login/")
def student_dashboard(request):
    student = getattr(request.user, "student_profile", None)

    if not student:
        raise PermissionDenied

    return render(
        request,
        "portfolio/student_dashboard.html",
        {"student": student}
    )


@login_required(login_url="/student/login/")
def student_logout(request):
    if request.method == "POST":
        logout(request)
        return redirect("student_login")

    return redirect("student_dashboard")