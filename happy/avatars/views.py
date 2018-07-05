from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework import status
from rest_framework.response import Response
from django.utils.translation import ugettext_lazy as _
from .serializers import UploadAvatarSerializer


class UploadAvatarView(RetrieveUpdateAPIView):

    serializer_class = UploadAvatarSerializer

    def get_object(self):
        return self.request.user

    def post(self, request, *args, **kwargs):
        # Create a serializer with request.data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        # Return the success message with OK HTTP status
        return Response(
            {"detail": _("Avatar has been changed.")},
            status=status.HTTP_200_OK
        )


upload_avatar_view = UploadAvatarView.as_view()
