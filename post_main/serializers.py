from rest_framework import serializers
from .models import PostComment, Video, Image, Tag, Post, Like, Reply
from user_controller.serializers import CustomUserSerializer

class TagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tag
        fields = ("title",)

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields ="__all__"

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields ="__all__"

class LikeSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only = True)
    
    class Meta:
        model = Like
        fields ="__all__"

class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        # print("yooooo::",dir(serializer.data))
        print("yoooaa::",serializer.data)

        return serializer.data
 
# # from rest_framework_recursive.fields import RecursiveField
# class PostCommentSerializer(serializers.ModelSerializer):
#     # post = PostSerializer(read_only=True)
#     post_id = serializers.IntegerField(write_only=True)
#     # author = CustomUserSerializer(read_only=True)
#     author_id = serializers.IntegerField(write_only = True)
#     reply = RecursiveSerializer(many=True, read_only=True)

#     class Meta:
#         model = PostComment
#         fields = "__all__"
from rest_framework_recursive.fields import RecursiveField


class ReplySerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    # to = "RecursiveSerializer"(read_only=True,many=True)
    # tocomment = serializers.RelatedField(many=True, read_only=True)
    # to_name = serializers.RelatedField(source='to', read_only=True,many=True)
    to = RecursiveField(many=False, read_only=True)
    author_id = serializers.IntegerField(write_only = True)
    to_id = serializers.IntegerField(write_only=True,required=False, allow_null=True)
    postcomment_id= serializers.IntegerField(write_only=True )
    # postcomment = PostCommentSerializer(read_only=True ,allow_null=True)

    class Meta:
        model = Reply
        fields = "__all__"


from django.db.models import Count

class PostSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    author_id = serializers.IntegerField(write_only = True)
    tags = TagSerializer(many=True, required=False)
    image = ImageSerializer(many=True, required=False)
    video = VideoSerializer(many=True, required=False)
    like  = LikeSerializer(many=True, required=False)
    comment_count= serializers.SerializerMethodField("get_comment_count")
    # comment = serializers.SerializerMethodField("get_comment")

    # def get_comment(self, obj):
    #     queryset = PostComment.objects.filter(post_id=obj.id, parent_id=None) 
    #     serializer = PostCommentSerializer(queryset, many=True)
    #     return serializer.data

    def get_comment_count(self, obj):
        count= 0
        a = obj.post_comment.all()
        count += a.count()
        for i in a:
            aa= i.reply.all().count()
            count += aa
        print("final count::", count)
        return count

    class Meta:
        model = Post
        fields = "__all__"

class PostCommentSerializer(serializers.ModelSerializer):
    post = PostSerializer(read_only=True)
    post_id = serializers.IntegerField(write_only=True)
    author = CustomUserSerializer(read_only=True)
    author_id = serializers.IntegerField(write_only = True)
    reply = ReplySerializer(many=True, read_only=True)

    class Meta:
        model = PostComment
        fields = "__all__"
  
# class PostSerializer(serializers.ModelSerializer):
#     author = CustomUserSerializer(read_only=True)
#     author_id = serializers.IntegerField(write_only = True)
#     tags = TagSerializer(many=True)
#     image = ImageSerializer(many=True)
#     video = VideoSerializer(many=True)
#     like  = LikeSerializer(many=True)
#     comment_count= serializers.SerializerMethodField("get_comment_count")
#     comment = serializers.SerializerMethodField("get_comment")

#     def get_comment(self, obj):
#         queryset = PostComment.objects.filter(post_id=obj.id, parent_id=None) 
#         serializer = PostCommentSerializer(queryset, many=True)
#         return serializer.data

#     def get_comment_count(self, obj):
#             return obj.post_comment.count()

#     class Meta:
#         model = Post
#         fields = "__all__"

