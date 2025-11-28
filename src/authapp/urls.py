from django.urls import path

from .api import RetrieveAccessToken, CreateUser
from .views import google_consent, google_callback, get_csrf

urlpatterns = [
    path('google/consent/', google_consent, name='google_consent'),
    path('google/callback/', google_callback, name='google_callback'),
    path('retrieve-access-token/', RetrieveAccessToken.as_view(), name='retrieve_access_token'),
    path('create/user', CreateUser.as_view(), name='create_user'),
    path("get-csrf/", get_csrf, name="get_csrf"),
]