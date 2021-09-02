import jwt
from .models import GenericFileUpload, Jwt, CustomUser
from datetime import datetime, timedelta
from django.conf import settings
import random
import string
from rest_framework.views import APIView
from .serializers import (
    LoginSerializer, SignupSerializer, RefreshSerializer, UserProfileSerializer, UserProfile, CustomUserSerializer
)
from django.contrib.auth import authenticate
from rest_framework.response import Response
from .authentication import Authentication
from litty.custom_methods import IsAuthenticatedCustom
from rest_framework.viewsets import ModelViewSet
import re
from django.db.models import Q, Count, Subquery, OuterRef
import json
from datetime import datetime, timedelta
from django.http import JsonResponse
from rest_framework.generics import ListAPIView
from .models import UserFollow
# pyjwt 1.7.1. used, 
def get_access_token(payload):
    print("payload:::::::::", payload)
    # exp = datetime.now().timestamp() + (exp * 60)
    exp = datetime.utcnow() + timedelta(minutes=10)
    return jwt.encode(
        {"exp": exp,
         **payload},
        settings.SECRET_KEY,
        algorithm="HS256"
    )

def get_refresh_token(payload):
    exp  = datetime.utcnow()+ timedelta(days=365)
    return jwt.encode(
        {"exp": exp, 
        **payload},
        settings.SECRET_KEY,
        algorithm="HS256"
    )

def decodeJWT(bearer):
    if not bearer:
        print("no bearer...")
        return None
    print("beeeeeeeeeaaaareeeeer:", bearer )
    try:
        token = bearer[7:]
    except Exception as e:
        print(e, "exceeeeeeption111")
    print("tokkkkkkkkkkkeeeeeeeeeeen:",token, )

    try:
        decoded = jwt.decode(token, key=settings.SECRET_KEY, algorithm = "HS256")#options= {"verify_signature":False})
    except jwt.DecodeError as e:
        print("Here1",e)
        decoded = None
    except Exception as e:
        print("Here2",e)
        decoded= None
   
    if decoded:
        try:
            print(CustomUser.objects.get(id=decoded["user_id"]), "iddddddddd")
            return CustomUser.objects.get(id=decoded["user_id"])
        except Exception as e:
            print(e," excepppppptionnnn2222")
            return None
    return None

class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password'])

        if not user:
            return Response({"error": "Invalid username or password"}, status="400")

        Jwt.objects.filter(user_id=user.id).delete()

        access = get_access_token({"user_id": user.id})
        refresh = get_refresh_token({"user_id": user.id})

        Jwt.objects.create(
            user_id=user.id, access=access.decode(), refresh=refresh.decode()
        )

        return Response({"access": access, "refresh": refresh})

# from django.core.files.base import ContentFile
from django.core.files import File as DjangoFile

class ProfilePic(APIView):
    permission_classes = (IsAuthenticatedCustom,)

    def post(self, request):
        try:
            print("request.data::::::", request.data)
            # serializer = self.serializer_class(data=request.data)
            # serializer.is_valid(raise_exception=True)
            image = request.data.pop("file_upload", None)
            print("image::",image)
            image= image[0]
            print("image222::",image)
        except Exception as e:
            print("propic error1:::",e)
            return Response({"error": "There was an error"}, status=400)

      
        try:
            qs  = image
            user = request.user
            user.user_picture = qs 
            user.save()
            try:
                pp = UserProfile.objects.get(user=user)
            except:
                pp = UserProfile.objects.create(user=user)
            pp.profile_picture = qs
            pp.is_verified= True
            pp.save()

            data = UserProfileSerializer(request.user.user_profile).data
            print("propic return data::::", data)
          
            # serializer = UserProfileSerializer(data=pp)
            # serializer.is_valid(raise_exception=True)
            # serializer= serializer
            # pi = serializer.profile_picture
            # pu = serializer.updated_at
            # profile = user.user_profile
            # profile.is_verified=True
            # profile.save()
        except Exception as e:
            print("propic error2:::",e)
            return JsonResponse({"error": "There was an error"}, status=400)

        return Response({"id":data.get("id"),"updated_at":data.get("updated_at"), "profile_picture":data.get("profile_picture")}, status=201)

class SignupView(APIView):
    serializer_class = SignupSerializer

    def post(self, request):
        print("request.data::::::", request.data)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
       #     serializer = self.serializer_class(data=request.data)
        #     serializer.is_valid()
        #     if not serializer:
        #         print("serializer error2:::", serializer.errors)

        username = serializer.validated_data.pop("username")
        email  =  serializer.validated_data.pop("email")


        try:
           check1  = CustomUser.objects.get(username = username)
        except:
            check1  = None
        if check1:
            return Response({"error": "user with this username already exist!"}, status=400)

        try:
            check2  = CustomUser.objects.get(email= email, is_verified=True)
        except:
            check2 = None
        if check2:
            return Response({"error": "email is already taken!"}, status=400)


        try:
            CustomUser.objects._create_user(username=username, email= email, **serializer.validated_data)
        except Exception as e:
            print(" error1::::", e)

        user  = CustomUser.objects.get(username = username)

        user_id = user.id
        token = get_refresh_token({"user_id": user.id}).decode()

        
        from django.contrib.sites.shortcuts import get_current_site
        from django.urls import reverse

        current_site  = get_current_site(request).domain
        relativeLink  = reverse("email-verify")
        # absurl = "http://"+ current_site + relativeLink  + "?token=" + str(token)
        bearer  = f"1bearer{str(token)}"
        absurl = "http://"+ current_site + relativeLink  + "?token=" + bearer
        email_body  = "Hi "+ user.username + " Click link below to verify your iHype account n/" + absurl + " Please do not proceed if this was sent to you by mistake!"
        data = {
            'domain':absurl,
            "email_body": email_body,
            'email_subject':"Please verify your email",
            "to_email":user.email
        }
        Util.send_email(data)
        return Response({"success": "User created."}, status=201)


class RefreshView(APIView):
    serializer_class = RefreshSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            active_jwt = Jwt.objects.get(
                refresh=serializer.validated_data["refresh"])
        except Jwt.DoesNotExist:
            print("refresh token not found")
            return Response({"error": "refresh token not found"}, status="400")
        except Exception as e:
            print(e)
        if not Authentication.verify_token(serializer.validated_data["refresh"]):
            print("token is invalid or expired")
            return Response({"error": "Token is invalid or has expired"})

        access = get_access_token({"user_id": active_jwt.user.id})
        refresh = get_refresh_token({"user_id": active_jwt.user.id})

        active_jwt.access = access.decode()
        active_jwt.refresh = refresh.decode()
        active_jwt.save()

        return Response({"access": access, "refresh": refresh})

class OtherProfile(APIView):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticatedCustom, )

    def get(self, request):
        try:
            data = {}
            keyword= request.GET.get('keyword', None)

            if keyword:
                user= CustomUser.objects.get(username= keyword)
                data = self.serializer_class(user.user_profile).data

            return Response(data, status=200)
  
        except Exception as e:
            print("UserprofileView error:::", e)

class UserProfileView(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticatedCustom, )

    def get_queryset(self):
        data = self.request.query_params.dict()
        keyword = data.get("keyword", None)

        if keyword:
            search_fields= (
                "user__username", "first_name", "last_name"
            )
            query = self.get_query(keyword, search_fields)
            print("unddderr")
            return self.queryset.filter(query).exclude(
                     Q(user_id=self.request.user.id) |
                     Q(user__is_superuser=True)).distinct()
        print("overrrrr")   
        return self.queryset
        # return self.queryset.exclude(
        #              Q(user_id=self.request.user.id) |
        #              Q(user__is_superuser=True))


    # def update(self, request, *args, **kwargs):
    #         try:
    #             request.data._mutable = True
    #         except:
    #             pass
    #         print("create profile",request.data)
           
            # a= request.data.get("author_id", None)    
            # b= request.user.id
            # print("ids:::", a,b)
            # # if str(request.user.id) != str(request.data.get("author_id", None)):
            # #     raise Exception("This user authorized to make this post")

            # serializer = self.serializer_class(data=request.data)
            # serializer.is_valid(raise_exception=True)
            # serializer.save()
        


    @staticmethod
    def get_query(query_string, search_fields):
        try:
            query = None  # Query to search for every search term
            terms = UserProfileView.normalize_query(query_string)
            for term in terms:
                or_query = None  # Query to search for a given term in each field
                for field_name in search_fields:
                    q = Q(**{"%s__icontains" % field_name: term})
                    if or_query is None:
                        or_query = q
                    else:
                        or_query = or_query | q
                if query is None:
                    query = or_query
                else:
                    query = query & or_query
            return query
        except Exception as e:
            print("errrror22")

    @staticmethod
    def normalize_query(query_string, findterms=re.compile(r'"([^"]+)"|(\S+)').findall, normspace=re.compile(r'\s{2,}').sub):
        return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]


class MeView(APIView):
    permission_classes = (IsAuthenticatedCustom, )
    serializer_class = UserProfileSerializer#CustomUserSerializer

    def get(self, request):
        data = {}
        try:
            data = self.serializer_class(request.user.user_profile).data
        except Exception:
            data = {
                "user": {
                    "id": request.user.id,
                    "is_verified":request.user.is_verified,
                    "username":request.user.username,

                    },
            }
        print("passing through meeeee  vieeeew")
        return Response(data, status=200)

  
#changed from api view to normal view
from django.views.generic import View
from django.http import HttpResponse
class VerifyEmail(View):
    # permission_classes = (IsAuthenticatedCustom, )

    def get(self, request):
        print("email verify request:::",request)
        token = request.GET.get('token')
        user= decodeJWT(token)
        if user: #and user.is_authenticated:
            user.is_verified = True
            user.save()
            try:
                check3  = CustomUser.objects.all().filter(email = user.email, verified=False)
                for a in check3:
                    if a.is_verified == False:
                        pass
                    else:
                        a.is_verified = False
                        a.email = ""
                        a.save()
            except:
                pass
           

            # return Response("success", status=200)
            return HttpResponse('''<body style='background:black;>
                    <p style='color:red'>Account verified successfully!</p>
                  
                    <a href='http://192.168.43.77:3000/' style='color:white; font-size:50px'>Account verified successfully! Login to continue!</a>
                    </body>''', status=200)

        return HttpResponse('''<body style='background:black;>
                    <p style='color:red'>Error, Action link expired!</p>
                    <a href='http://192.168.43.77:3000/' style='color:white; font-size:50px'>Error, Action link expired </a>
                    </body>''', status=200)





class LogoutView(APIView):
    permission_classes = (IsAuthenticatedCustom, )

    def get(self, request):
        user_id = request.user.id

        Jwt.objects.filter(user_id=user_id).delete()

        return Response("logged out successfully", status=200)

from django.core.mail import EmailMessage
class Util:
    @staticmethod
    def send_email(data):
        try:
            email = EmailMessage(
                subject= data['email_subject'],
                body = data['email_body'],
                to = [data['to_email']],
                )
            email.send()
            print("Sent email to:::", data['to_email'])
        except Exception as e:
            print("Util error:::", e)

from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .serializers import ResetPasswordEmailRequestSerializer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

class RequestPasswordByEmail(APIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        # data = {'request': request, 'data':request.data }
        serializer = self.serializer_class(data = request.data)
        try:
            email = request.data['email']
            if CustomUser.objects.filter(email = email, is_verified= True).exists():
                user = CustomUser.objects.get(email=email, is_verified=True)
                print("password reset request by::::::",user)
                uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
                token = PasswordResetTokenGenerator().make_token(user)

                current_site  = get_current_site(request=request).domain
                relativeLink  = reverse("password-reset-confirm", kwargs = {'uidb64':uidb64, 'token':token})
                absurl = "http://"+ current_site + relativeLink 
                email_body  = "Hi, \n  Use this link to reset your password \n" + absurl + " Please do not proceed if this was sent to you by mistake!"
                data = {
                    'domain':absurl,
                    "email_body": email_body,
                    'email_subject':"Password Reset",
                    "to_email":user.email
                }
             
                Util.send_email(data)

            return Response({"success":"We have sent you a link to reset your password"}, status= 200)
        except Exception as e:
            print("error password reset:::::",e)
        return Response({"success": "We have have sent you a link to reset your password"}, status= 200)


from django.shortcuts import render
class PasswordTokenCheck(APIView):
    def get(self, request, uidb64, token):
        try:
            id  = smart_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(id = id)

            if not  PasswordResetTokenGenerator().check_token(user, token):
                context = {
                    "error":"The token aint valid or has expired, please request a new password reset!!!"               
                     }
                return render(request, "user_controller/dashbase.html", context)

            context = {
                    "success":True, 
                    "message":"Credentials is valid", 
                    "uidb64":uidb64, 
                    "token":token  
                                  }
            return render(request, "user_controller/dashbase.html", context)

        except DjangoUnicodeDecodeError as e:
            context = {
                    "error":"The token aint valid or has expired , please request a new password reset!!!"               
                     }
            return render(request, "user_controller/dashbase.html", context)

        except Exception as e:
            print("password token check::::", e)

# from .serializers import FinalSetNewPasswordSerializer

from .serializers import FinalSetNewPasswordSerializer
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator
# @method_decorator(csrf_exempt, name='dispatch')
class FinalSetNewPassword(APIView):
    serializer_class = FinalSetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        
        return Response({"success":True, "message":"Your password has been reset successfully. Go back to login page to continue!!"}, status = 200)



class SecondaryEmailVerification(APIView):
    permission_classes = (IsAuthenticatedCustom, )

    def post(self, request):
        user = request.user
       
        token = get_refresh_token({"user_id": user.id}).decode()

        current_site  = get_current_site(request).domain
        relativeLink  = reverse("email-verify")
        # absurl = "http://"+ current_site + relativeLink  + "?token=" + str(token)
        bearer  = f"1bearer{str(token)}"
        absurl = "http://"+ current_site + relativeLink  + "?token=" + bearer
        email_body  = "Hi "+ user.username + " Click link below to verify your iHype account n/" + absurl + " Please do not proceed if this was sent to you by mistake!"
        data = {
            'domain':absurl,
            "email_body": email_body,
            'email_subject':"Please verify your email",
            "to_email":user.email
        }
        Util.send_email(data)
        return Response({"success": "User created."}, status=201)


from django.contrib.auth.hashers import check_password
from .serializers import ChangePasswordSerializer

class ChangePassword(APIView):
    permission_classes = (IsAuthenticatedCustom, )
    serializer_class  = ChangePasswordSerializer

    def post(self, request):
        user = request.user
        syspassword= user.password #user's current password

        try:
            serializer= self.serializer_class(data = request.data)
            serializer.is_valid(raise_exception=True)
            
            currentPassword = serializer.validated_data.pop("currentPassword")
            confirmPassword = serializer.validated_data.pop("confirmPassword")
        

            matchcheck= check_password(currentPassword, syspassword)
            if matchcheck:
                print("Its a match")
                user.set_password(confirmPassword) 
                user.save()
                return Response({"success": "Password changed."}, status=201)
            return Response({"error": "passwords dont match."}, status=401)
        except Exception as e:
            print("change password:::", e)



class UpdateFollowListView(ListAPIView):
    permission_classes = (IsAuthenticatedCustom,)


    def post(self, request, *args, **kwargs):
        print("request.data::::", request.data)
        other_id = request.data.get("other_id")
        user = request.user

        if other_id:
            try:
                other_user = CustomUser.objects.get(id=other_id)
                print("otheruser:::::",other_user)

            except Exception as e:
                print("updateFollowError 1:::::",e)
             
            try:
                me = user.user_profile
                print("me:::", me)
                o_user = other_user.user_profile
                print("o_other", o_user)

                try:
                    me_fol = UserFollow.objects.get(user=user)
                    print("me_fol:::", me_fol)
                except:
                    me_fol = UserFollow.objects.create(user=user)
                try:
                    other_fol = UserFollow.objects.get(user=other_user)
                    print("other_fol:::", other_fol)
                except:
                    other_fol = UserFollow.objects.create(user=other_user)
                
               
             
            except Exception as e:
                print("updateFollowError 2:::::",e)
                 
            try:
                print("mefollowwers.all:::",me.followers.all())
                print("mefollowing.all:::",me.following.all())

                if other_fol in me.following.all():
                    print("removing follower")
                    me.following.remove(other_fol)
                    o_user.followers.remove(me_fol)
                    print("removed follower")
                    return JsonResponse({"data":"unfollowed"})
                else:
                    print("adding follower")
                    me.following.add(other_fol)
                    print("1")
                    o_user.followers.add(me_fol)
                    print("added follower")
                    return JsonResponse({"data":"followed"})

            except Exception as e:
                print("updateFollowError 3::::", e)

        return JsonResponse({"data":"nothing"})




class GetFollowingChat(APIView):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticatedCustom, )

    def get(self, request):
        try:
            data = {}
            # keyword= request.GET.get('keyword', None)

            if request.user:
                # user= CustomUser.objects.get(username= request.user)
                data = self.serializer_class(request.user.user_profile).data
                print("data:::", data)
            return Response(data, status=200)
  
        except Exception as e:
            print("GetFollowingChatError:::", e)


