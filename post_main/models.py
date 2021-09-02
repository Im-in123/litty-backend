from django.db import models
from django.core.validators import FileExtensionValidator




class Tag(models.Model):
    title = models.CharField(max_length= 50, unique=True)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return  f"{self.title} Tag"

class Image(models.Model):
    post= models.ForeignKey("Post", related_name="image_post_link", on_delete= models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    image = models.ImageField( upload_to="post_images", default='default.jpg')


    def __str__(self):
        return  f"{self.post.author} Image"

class Video(models.Model):
    post= models.ForeignKey("Post", related_name="video_post_link", on_delete= models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    video = models.FileField(upload_to='episodes_uploaded',null=True, blank=True, \
                 validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])])
    

    def __str__(self):
        return  f"{self.post.author} Video"

class Like(models.Model):
    user= models.ForeignKey("user_controller.CustomUser", related_name="like_user", on_delete= models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)


    def __str__(self):
        return  f"{self.user.username} Like"

class Post(models.Model):
    author = models.ForeignKey("user_controller.CustomUser", related_name="post_author", on_delete= models.CASCADE)
    caption = models.CharField(max_length= 100)
    tags = models.ManyToManyField(Tag, related_name="post_tag", blank=True)
    image = models.ManyToManyField(Image, related_name="post_image", blank=True)
    video = models.ManyToManyField(Video, related_name="post_video", blank=True)
    like = models.ManyToManyField(Like, related_name="post_like", blank=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return  f"{self.author}-{self.caption} Post"


# class PostComment(models.Model):
#     author = models.ForeignKey("user_controller.CustomUser", related_name="post_comment_author", on_delete=models.CASCADE)
#     post = models.ForeignKey(Post, related_name="post_comment", on_delete=models.CASCADE)
#     comment = models.TextField()
#     created_at = models.DateTimeField(auto_now_add = True)
#     updated_at = models.DateTimeField(auto_now = True)
#     parent = models.ForeignKey('self', null=True, blank=True, related_name='reply', on_delete=models.CASCADE)
#     like = models.ManyToManyField("user_controller.CustomUser", blank=True, related_name='comment_like')

#     class Meta:
#         ordering = ("-created_at",)
    
#     def __str__(self):
#         return f"{self.comment} - {self.author.username} Comment"

#     @property
#     def children(self):
#         return PostComment.objects.filter(parent=self).order_by('-created_on').all()    

#     @property
#     def is_parent(self):
#         if self.parent is None:
#             return True
#         return False
class Reply(models.Model):
    author = models.ForeignKey("user_controller.CustomUser", related_name="post_comment_reply_author", on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    like = models.ManyToManyField("user_controller.CustomUser", blank=True, related_name='comment_reply_like')
    to = models.ForeignKey("self", related_name="tocomment", on_delete=models.CASCADE, null=True, blank=True)
    postcomment = models.ForeignKey("PostComment", related_name="postcomment_reply", on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ("created_at",)
    

class PostComment(models.Model):
    author = models.ForeignKey("user_controller.CustomUser", related_name="post_comment_author", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="post_comment", on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    # parent = models.ForeignKey('self', null=True, blank=True, related_name='reply', on_delete=models.CASCADE)
    like = models.ManyToManyField("user_controller.CustomUser", blank=True, related_name='comment_like')
    reply= models.ManyToManyField(Reply, blank=True, related_name='comment_reply')

    class Meta:
        ordering = ("created_at",)
    
    def __str__(self):
        return f"{self.comment} - {self.author.username} Comment"

    

