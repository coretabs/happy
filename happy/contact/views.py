from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ContactSerializer
from rest_framework.permissions import AllowAny



class ContactView(GenericAPIView):

    serializer_class = ContactSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        # Create a serializer with request.data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        # Return the success message with OK HTTP status
        return Response(
            {'detail': ("Thanks for contacting us")},
            status=status.HTTP_200_OK
        )


contact_view = ContactView.as_view()