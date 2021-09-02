from django.contrib import admin

# Register your models here.
from .models import Message, MessageAttachment, GenericFileUpload, ChatList

admin.site.register((Message, MessageAttachment, ChatList, GenericFileUpload,))