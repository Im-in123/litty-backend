from django.urls import path, include
from .views import (
    LoginView, SignupView, RefreshView, UserProfileView, MeView, LogoutView, VerifyEmail,  RequestPasswordByEmail,PasswordTokenCheck, FinalSetNewPassword, SecondaryEmailVerification, ChangePassword, OtherProfile, ProfilePic, UpdateFollowListView, GetFollowingChat

    
)
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from django.conf import settings

router = DefaultRouter(trailing_slash=False)

router.register("profile", UserProfileView)

urlpatterns = [
    path('', include(router.urls)),
    path('login', LoginView.as_view()),
    path('signup', SignupView.as_view()),
    path('refresh', RefreshView.as_view()),
    path('me', MeView.as_view()),
    path('propic-upload', ProfilePic.as_view()),
    path('otherprofile', OtherProfile.as_view()),
    path('logout', LogoutView.as_view()),
    path('email-verify', VerifyEmail.as_view(), name="email-verify"),
    path('request-reset-password', RequestPasswordByEmail.as_view(), name="request-reset-password"),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordTokenCheck.as_view(), name="password-reset-confirm"),
    path('password-reset-complete', FinalSetNewPassword.as_view(), name="password-reset-complete"),
    path('secondary-email-verification', SecondaryEmailVerification.as_view()),
    path('change-password', ChangePassword.as_view()),
    path('update-follow', UpdateFollowListView.as_view()),
    path('get-following-chat', GetFollowingChat.as_view()),





]
if settings.DEBUG:

    #urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)