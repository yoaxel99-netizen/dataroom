import requests
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.files.base import ContentFile

from authapp.views import CsrfExemptSessionAuthentication
from .models import Storage
from authapp.models import AuthToken


class StorageList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        stored_objects = Storage.objects.filter(user=request.user).order_by("-uploaded_at")

        storage_list = [
            {
                "uid": str(stored_object.uid),
                "name": stored_object.name,
                "mimeType": stored_object.mimeType,
                "uploaded_at": stored_object.uploaded_at.isoformat(),
            }
            for stored_object in stored_objects
        ]

        return Response(storage_list)


class StorageSave(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            token = AuthToken.objects.get(user=request.user)
            access_token = token.access_token

            file_id = request.data.get("id")
            name = request.data.get('name')
            mime_type = request.data.get('mimeType')

            headers = {
                "Authorization": f"Bearer {access_token}",
                "apikey": "AIzaSyCKa4n1mg7-h-pwe0JQzaDSiRkYYr4tT9o"
            }
            url = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media"
            response_api = requests.get(url, headers=headers)
            response_api.raise_for_status()

            storage_object = Storage.objects.create(
                user=request.user,
                name=name,
                mimeType=mime_type,
            )
            storage_object.file.save(name, ContentFile(response_api.content), save=True)

            return Response({"status": "File saved successfully!", "id": storage_object.uid}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StorageDelete(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, uid, *args, **kwargs):
        try:
            storage_object = Storage.objects.get(uid=uid)
            if storage_object.file:
                storage_object.file.delete(save=False)
            storage_object.delete()
            return Response({"status": "File deleted successfully!"}, status=status.HTTP_200_OK)

        except Storage.DoesNotExist as e:
            return Response({"status": f"File not found! {str(e)}"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Hello from Django DRF!"})
