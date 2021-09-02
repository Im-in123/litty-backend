from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.utils import timezone
from rest_framework.views import exception_handler
from rest_framework.response import Response
from django.contrib.auth import authenticate


class IsAuthenticatedCustom(BasePermission):

    def has_permission(self, request, view):
        try:

            from user_controller.views import decodeJWT

            print(request, "requeeeeeessssst")
            print(request.data, "dataaaaaaa")
            print(request.META['HTTP_AUTHORIZATION'], "meeeetttttaaaaaa")

            #user = decodeJWT(request)
            #print(user)
            user = decodeJWT(request.META['HTTP_AUTHORIZATION'])
            if not user:
                return  False
            request.user = user
            print(request.user, 'requeeeest....usssserr')
            if request.user and request.user.is_authenticated:
                print("user is authenticated")
                from user_controller.models import CustomUser
                try:
                    CustomUser.objects.filter(id=request.user.id).update(
                        is_online=timezone.now())
                    print("yaaaah")
                    return True
                except Exception as e:
                    print(e, "errrroooooor")
                
            return False
        except Exception as e:
            print("IsAuthenticatedError::::", e)
            return False


class IsAuthenticatedOrReadCustom(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            print("hidden....")
            return True

        if request.user and request.user.is_authenticated:
            print("hidden")
            from user_control.models import CustomUser
            CustomUser.objects.filter(id=request.user.id).update(
                is_online=timezone.now())
            return True
        return False


def custom_exception_handler(exc, context):
            
    print("hidden")

    response = exception_handler(exc, context)

    if response is not None:
        return response

    exc_list = str(exc).split("DETAIL: ")

    return Response({"error": exc_list[-1]}, status=403)
