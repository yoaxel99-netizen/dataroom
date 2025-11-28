import environ
import pprint
from django.contrib.auth.decorators import login_required
from rest_framework.authentication import SessionAuthentication
from django.conf import settings
from django.shortcuts import redirect
from google_auth_oauthlib.flow import Flow
from django.http import HttpResponseBadRequest
from .models import AuthToken
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from django.contrib.auth.models import User
from django.contrib.auth import login


env = environ.Env()
pp = pprint.PrettyPrinter(indent=4)


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


@login_required
def google_consent(request):
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uris": [settings.GOOGLE_REDIRECT_URI],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=[
            "https://www.googleapis.com/auth/drive.readonly",
        ],
    )

    flow.redirect_uri = settings.GOOGLE_REDIRECT_URI

    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
    )

    request.session["oauth_state"] = state

    return redirect(authorization_url)


@login_required
def google_callback(request):
    state = request.session.get("oauth_state")
    incoming_state = request.GET.get("state")

    if state != incoming_state:
        return HttpResponseBadRequest("Invalid state parameter.")

    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uris": [settings.GOOGLE_REDIRECT_URI],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=[
            "https://www.googleapis.com/auth/drive.readonly",
        ],
        state=state
    )

    flow.redirect_uri = settings.GOOGLE_REDIRECT_URI

    authorization_response = request.build_absolute_uri()
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials

    # user = request.user
    info = id_token.verify_oauth2_token(credentials.id_token, google_requests.Request(), settings.GOOGLE_CLIENT_ID)
    google_email = info["email"]
    user, created = User.objects.get_or_create(
        username = google_email,
        defaults = {"email": google_email}
    )
    login(request, user)

    # print(f"Credentials: {credentials}")

    token_obj, _ = AuthToken.objects.update_or_create(
        user=user,
        defaults={
            "access_token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "expires_at": credentials.expiry,
        }
    )

    if "oauth_state" in request.session:
        del request.session["oauth_state"]

    return redirect(env("NEXTJS_URL"))

