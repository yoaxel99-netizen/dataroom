from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import AuthToken


class RetrieveAccessToken(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        token = AuthToken.objects.get(user=request.user)
        return Response({"access_token": token.access_token})
