from django.urls import path
from storage.api import TestAPIView, StorageSave, StorageDelete, StorageList
from storage.views import TestGoogleDriveStorage

urlpatterns = [
    path('test/', TestAPIView.as_view(), name='test-api'),
    path('google-drive/test/', TestGoogleDriveStorage.as_view(), name='google-drive-test-api'),
    path('list/', StorageList.as_view(), name='storage-list'),
    path('save/', StorageSave.as_view(), name='storage-save'),
    path('delete/<str:uid>', StorageDelete.as_view(), name='storage-delete'),
]