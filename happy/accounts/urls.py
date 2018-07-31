from django.urls import path, include
from avatars.views import upload_avatar_view


from allauth.account.views import confirm_email as allauthemailconfirmation
from rest_framework_jwt.views import obtain_jwt_token

from .views import (FacebookLogin, 
                   UserProfileView,
                   UserPostsView,logout_view,
                   user_details_view,
                   resend_confirmation_view,
                   verify_email,
                   GetUserProfile)

urlpatterns = [
    path(r'', include('rest_auth.urls')),
    path(r'facebook/', FacebookLogin.as_view(), name='fb_login'),
    path(r'token/', obtain_jwt_token),
    path(r'logout/', logout_view),
    path(r'user/', user_details_view),
    path(r'user/avatar/', upload_avatar_view),
    path(r'user/profile/', UserProfileView.as_view()),
    path(r'user/posts/', UserPostsView.as_view()),
    path(r'registration/', include('rest_auth.registration.urls')),
    path(r'confirmation/', resend_confirmation_view),
    #path(r'registration/verify-email/', verify_email),

    path(r'user/<username>/', GetUserProfile.as_view({'get': 'retrieve'})),

]
