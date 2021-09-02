from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from .views import ChatListView
from user_controller.serializers import CustomUserSerializer

router = DefaultRouter(trailing_slash =True)
router.register("chatlist", ChatListView)



urlpatterns = [
    path("", include(router.urls)),
   
    # path("like-view", LikeControl.as_view()),
    # path("post-delete", CustomPostDelete.as_view()),

    # path("movie-videos/<int:blog_id>", SimilarVideos.as_view())
]
if settings.DEBUG:

    #urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)