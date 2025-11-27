import requests
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class TestGoogleDriveStorage(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        access_token = user.authtoken.access_token
        headers_api = {
            "Authorization": f"Bearer {access_token}",
        }
        response_api = requests.get(
            "https://www.googleapis.com/drive/v3/files",
            headers=headers_api,
        )

        return Response({"response": response_api.json()})
