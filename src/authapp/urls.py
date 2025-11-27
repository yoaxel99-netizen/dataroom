from django.urls import path

from .api import RetrieveAccessToken
from .views import google_consent, google_callback

urlpatterns = [
    path('google/consent/', google_consent, name='google_consent'),
    path('google/callback/', google_callback, name='google_callback'),
    path('retrieve-access-token/', RetrieveAccessToken.as_view(), name='retrieve_access_token'),
]