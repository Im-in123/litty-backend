from rest_framework import serializers
from .models import UserProfile, CustomUser, GenericFileUpload, UserFollow
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.exceptions import AuthenticationFailed

class GenericFileUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = GenericFileUpload
        fields = "__all__"


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField()


class RefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()

# class ImagSerializer(serializers.Serializer):
#     class Meta:
#         model = Imag
#         fields = "__all__"


class CustomUserSerializer(serializers.ModelSerializer):
    # user_picture = serializers.SerializerMethodField("get_img")
    # user_picture = serializers.ImageField(read_only=True, use_url=True)
    
    user_picture_id = serializers.IntegerField(
        write_only=True, required=False)
        
    class Meta:
        model = CustomUser
        exclude = ("password", )

  
    # def get_img(self, obj):
    #     return obj.user_picture.url
class UserFollowSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = UserFollow
        fields = "__all__"

class UserProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    profile_picture = serializers.ImageField(read_only=True)
    followers= UserFollowSerializer(many=True)
    following=UserFollowSerializer(many=True)
    # profile_picture_id = serializers.IntegerField(
    #     write_only=True, required=False)
    # message_count = serializers.SerializerMethodField("get_message_count")

    class Meta:
        model = UserProfile
        fields = "__all__"

    # def get_message_count(self, obj):
    #     try:
    #         user_id = self.context["request"].user.id
    #     except Exception as e:
    #         user_id = None

    #     from message_control.models import Message
    #     message = Message.objects.filter(sender_id=obj.user.id, receiver_id=user_id, is_read=False).distinct()

    #     return message.count()


# class FavoriteSerializer(serializers.Serializer):
#     favorite_id = serializers.IntegerField()

class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ['email']



class FinalSetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length = 6, max_length = 68, write_only= True) #doesnt return the password, writeonly
    token = serializers.CharField(min_length = 1,write_only= True)  
    uidb64 = serializers.CharField(min_length = 1, write_only= True) 

    class Meta:
        fields = "__all__"

    def validate(self, attrs):

        try:
            password  = attrs.get('password')
            token  = attrs.get('token')
            uidb64 = attrs.get('uidb64')
            idd = force_str((urlsafe_base64_decode(uidb64)))
            user = CustomUser.objects.get(id = idd)
            if not  PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed("The reset link is invalid, if it has already been used request a new one!!", 401) 
            user.set_password(password) 
            user.save()
            return (user)

        except Exception as e:
            print("Serializer Finalsetnewpassword::::", e)
            raise AuthenticationFailed("The reset link is invalid, if it has already been used request a new one!!", 401)  
        return super().validate(attrs)          


class ChangePasswordSerializer(serializers.Serializer):
    currentPassword  = serializers.CharField()
    password = serializers.CharField()
    confirmPassword = serializers.CharField()

    class Meta:
        fields = "__all__"
