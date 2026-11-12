
from django.shortcuts import redirect
from django.urls import reverse

from .models import MFADevice


class AdminMFAMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if (
            request.path.startswith("/admin/")
            and request.user.is_authenticated
            and request.user.is_staff
        ):

            verified = (
                request.session.get("mfa_verified") is True
                and request.session.get("mfa_verified_user_id")
                == request.user.pk
            )

            if not verified:

                mfa_enabled = MFADevice.objects.filter(
                    user=request.user,
                    enabled=True
                ).exists()

                if mfa_enabled:
                    return redirect(reverse("mfa_challenge"))

                return redirect(reverse("mfa_setup"))

        return self.get_response(request)