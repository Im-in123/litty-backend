

from rest_framework import serializers
from .models import GenericFileUpload, Message, MessageAttachment, ChatList
from user_controller.serializers import CustomUserSerializer


class GenericFileUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = GenericFileUpload
        fields = "__all__"


class MessageAttachmentSerializer(serializers.ModelSerializer):
    attachment = GenericFileUploadSerializer()

    class Meta:
        model = MessageAttachment
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField("get_sender_data")
    sender_id = serializers.IntegerField(write_only=True)
    receiver = serializers.SerializerMethodField("get_receiver_data")
    receiver_id = serializers.IntegerField(write_only=True)
    message_attachments = MessageAttachmentSerializer(
        read_only=True, many=True)

    class Meta:
        model = Message
        fields = "__all__"

    def get_receiver_data(self, obj):
        from user_controller.serializers import UserProfileSerializer
        return UserProfileSerializer(obj.receiver.user_profile).data

    def get_sender_data(self, obj):
        from user_controller.serializers import UserProfileSerializer
        return UserProfileSerializer(obj.sender.user_profile).data


class ChatListSerializer(serializers.Serializer):
    user = CustomUserSerializer(read_only=True)
    user_id = serializers.IntegerField()
    other = CustomUserSerializer(read_only=True)
    other_id = serializers.IntegerField()

    class Meta:
        model = ChatList
        fields = "__all__"