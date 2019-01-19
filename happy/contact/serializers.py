from rest_framework import serializers
from django.conf import settings
from django.core.mail import send_mail


class ContactSerializer(serializers.Serializer):
    sender_name = serializers.CharField(required=True, max_length=100)
    mail_body = serializers.CharField(required=True)

    def save(self):
        name = self.validated_data['name']
        message = self.validated_data['body']
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['grinn.contactus@gmail.com',]
        send_mail( name, message, email_from, recipient_list )