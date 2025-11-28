from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings
from django.shortcuts import redirect
from google_auth_oauthlib.flow import Flow
from django.http import HttpResponseBadRequest, JsonResponse
from .models import AuthToken
import environ
import pprint


env = environ.Env()
pp = pprint.PrettyPrinter(indent=4)


@ensure_csrf_cookie
def get_csrf(request):
    return JsonResponse({"message": "CSRF Cookie Set"})


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

    user = request.user

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

