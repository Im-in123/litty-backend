from django.urls import path, include
from .views import VideoView,  TagView, PostView, ImageView, CommentView, LikeView, LikeControl, GenericFileUploadView, CustomPostDelete, ReplyView
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter(trailing_slash =True)
router.register("post", PostView)
router.register("video", VideoView)
router.register("image", ImageView)
router.register("tag", TagView)
router.register("comment", CommentView)
router.register("like", LikeView)
router.register("reply", ReplyView)
router.register("file-upload", GenericFileUploadView)



urlpatterns = [
    path("", include(router.urls)),
   
    path("like-view", LikeControl.as_view()),
    path("post-delete", CustomPostDelete.as_view()),

    # path("movie-videos/<int:blog_id>", SimilarVideos.as_view())
]
if settings.DEBUG:

    #urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)