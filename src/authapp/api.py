from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import AuthToken


class RetrieveAccessToken(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        token = AuthToken.objects.get(user=request.user)
        return Response({"access_token": token.access_token})


class CreateUser(APIView):

    def post(self, request):
        password = request.data.get("password")

        user = User.objects.create_user(
            username = 'dataroom',
            email = 'dataroom@datarom.com',
            is_superuser = True,
            is_staff = True,
            is_active = True,
            password = password,
        )
        user.save()

        return Response({"user": user})
