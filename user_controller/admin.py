from django.contrib import admin
from .models import CustomUser, Jwt, UserFollow,  UserProfile, GenericFileUpload


admin.site.register((CustomUser, Jwt, ))
admin.site.register((UserProfile, UserFollow))
admin.site.register(GenericFileUpload)
