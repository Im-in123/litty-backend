from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

class GenericFileUpload(models.Model):
    file_upload = models.FileField( upload_to='user_and_profile_image')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file_upload}"

class CustomUserManager(BaseUserManager):

    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError("Username field is required")

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=100)
    email = models.EmailField()
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_online = models.DateTimeField(default=timezone.now)
    user_picture = models.ImageField(upload_to="user_pics", blank=True, null=True, default='default.jpg')
    USERNAME_FIELD = "username"
    objects = CustomUserManager()

    def __str__(self):
        return self.username

    class Meta:
        ordering = ("created_at",)


class UserFollow(models.Model):
    user = models.ForeignKey(
        CustomUser, related_name="user_follow", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.username

from django.core.validators import RegexValidator
class UserProfile(models.Model):
    user = models.OneToOneField(
        CustomUser, related_name="user_profile", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    bio = models.TextField()
    city = models.CharField(max_length=100)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
    is_verified  = models.BooleanField(default=False)
    followers= models.ManyToManyField(UserFollow, related_name="profile_follower", blank=True)
    following= models.ManyToManyField(UserFollow, related_name="profile_following", blank=True)
    profile_picture =  models.ImageField(upload_to="profile_pics", blank=True, null=True, default='default.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ("created_at",)

# class Imag(models.Model):
#     image= models.ImageField(upload_to="here")

class Jwt(models.Model):
    user = models.OneToOneField(
        CustomUser, related_name="login_user", on_delete=models.CASCADE)
    access = models.TextField()
    refresh = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
