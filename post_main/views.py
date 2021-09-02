from django.shortcuts import render
from .serializers import PostSerializer,  TagSerializer, ImageSerializer, VideoSerializer, PostCommentSerializer, LikeSerializer, ReplySerializer
from .models import  Video, Image, Tag, Post, PostComment, Like, Reply
from rest_framework.viewsets import ModelViewSet
from user_controller.models import CustomUser
from rest_framework.generics import ListAPIView
from django.http import JsonResponse
from litty.custom_methods import IsAuthenticatedCustom
from user_controller.models import GenericFileUpload
from user_controller.serializers import GenericFileUploadSerializer
from rest_framework.views import APIView

# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator
# @method_decorator(csrf_exempt, name='dispatch')


class GenericFileUploadView(ModelViewSet):
    queryset = GenericFileUpload.objects.all()
    serializer_class = GenericFileUploadSerializer


class PostView(ModelViewSet):
    queryset = Post.objects.all()
    # queryset = Message.objects.select_related(
    #     "sender", "receiver").prefetch_related("message_attachments")
    # blogs =self.queryset.annotate(comment_count=Count("blog_comments")).order_by("-comment_count")[:5]

    permission_classes = (IsAuthenticatedCustom,)
    # pagination_class = PaginationInterface
    serializer_class = PostSerializer
    lookup_field = "id"

    def get_queryset(self):
        try:
            self.queryset = Post.objects.all()
            query = self.request.query_params.dict()
            username = query.get("keyword", None)
            if username:
                print("keyword::::", username)
                user  = CustomUser.objects.get(username = username)
                print("user::::", user)
                print("username::::", user.username)

                query_data = self.queryset.filter(author = user)
                return query_data
            return self.queryset
        except Exception as e:
            print("PostView Error:::", e)
            # return self.
            
    def create(self, request, *args, **kwargs):
        try:
            request.data._mutable = True
        except:
            pass
        print("create post",request.data)
        # c= self.request.FILES.getlist('image')
        # print("c::::",c)
        # v=  request.data.getlist('images')
        # print("v::::",v)
        images = request.data.pop("image", None)
        a= request.data.get("author_id", None)    
        b= request.user.id
        print("ids:::", a,b)
        if str(request.user.id) != str(request.data.get("author_id", None)):
            raise Exception("This user authorized to make this post")

        print("images:::",images)
        # for i in images:
        #     print("i::",i)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        # if images:
        #     Image.objects.bulk_create([Image(
        #     **image, post_id=serializer.data["id"]) for image in images])
        if images:
            post=Post.objects.get(id=serializer.data["id"])
            for a in images:
                q = Image.objects.create(image=a, post_id=serializer.data["id"])
                post.image.add(q)
                post.save()
        return JsonResponse({"data":"success"})

    # many = True if isinstance(request.data, list) else False
    # serializer = BookSerializer(data=request.data, many=many)
    # serializer.is_valid(raise_exception=True)
    # author = request.user # you can change here
    # book_list = [Book(**data, author=author) for data in serializer.validated_data]
    # Book.objects.bulk_create(book_list)
    # return Response({}, status=status.HTTP_201_CREATED)

class ImageView(ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

class VideoView(ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

class TagView(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class LikeView(ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class CommentView(ModelViewSet):
    queryset = PostComment.objects.all()#.filter(parent_id = None)
    serializer_class = PostCommentSerializer

    def get_queryset(self):
        query =self.request.query_params.dict()
        return self.queryset.filter(**query)

class LikeControl(ListAPIView):
    permission_classes = (IsAuthenticatedCustom,)
    
    def post(self, request, *args, **kwargs):
      
        try:
            post_id = request.data.get("post_id")
            user= request.user
            try:
                qs= Post.objects.get(id=post_id)
                # print(dir(qs.like))
                try:
                    like  = Like.objects.get(user=request.user)
                    print(like)
                    print(qs.like.all())
                    if like in qs.like.all():
                        qs.like.remove(like)
                        return JsonResponse({"data":"success-removed"})
                    else:
                        qs.like.add(like)
                        return JsonResponse({"data":"success-added"})

                except Exception as e:
                    print(e)
                    like = Like.objects.create(user= user)
                    qs.like.add(like)
                    return JsonResponse({"data":"success-added1"})
                
               
            except Exception as e:
                print(e)
                return JsonResponse({"data":"error"})

        except Exception as e:
            print("LikeController error::::", e)
 
class CustomPostDelete(APIView):
    permission_classes = (IsAuthenticatedCustom,)
    
    def post(self, request, *args, **kwargs):
        try:
            post_id = request.data.get("post_id")
            user= request.user
            author_id = request.data.get("author_id", None)

            if str(user.id) != str(author_id):
                # raise Exception("This user authorized to delete this post")
                print("This user authorized to delete this post")
                return JsonResponse({"data":"This user authorized to delete this post"})

            qs  = Post.objects.get(id =post_id, author=user)
            qs.delete()
            return JsonResponse({"data":"delete-successful"})
        except Exception as e:
            print("PostDelete error:::",e)
            return JsonResponse({"data":"error"})

class ReplyView(ModelViewSet):
    permission_classes = (IsAuthenticatedCustom,)
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer

    def get_queryset(self):
        try:
            user= self.request.user
            # self.queryset = Reply.objects.all().filter(author=user)
            query = self.request.query_params.dict()
            comment_id= query.get("comment_id", None)
            post_id= query.get("post_id", None)
            print("user::::", user)
            print("comment_id::::", comment_id)
            print("post_id::::", post_id)

            if user and comment_id:
                comment = PostComment.objects.get(id=comment_id)
                query_data = Reply.objects.all().filter(postcomment=comment)
                return query_data
            return None

        except Exception as e:
            print("ReplyView Error:::", e)

    def create(self, request):
        try:
            request.data._mutable = True
        except:
            pass
        print("replydata",request.data)
        try:
            user= request.user
            query = request.data
            type= query.get("type", None)

            if type=="comment-reply":
                comment_id= query.get("comment_id", None)
                comment= query.get("comment", None)
                # post_id= query.get("post_id", None)
                print("comment_id::::", comment_id)
                print("comment::::", comment)


                if user and comment_id:
                    

                    author_id= user.id
                    # to_id= 
                    postcomment_id = comment_id
                    # comment= 
                    mydata ={
                        "author_id":author_id,
                        "postcomment_id":postcomment_id,
                        "comment":comment
                    }

                    data1 = self.serializer_class(data= mydata)
                    data1.is_valid(raise_exception=True)
                    data1.save()
                    data=data1.data
                    print("data1::",data)
                    qid= data.get("id")
                    print("qid::",id)

                    qs = PostComment.objects.get(id=comment_id)
                    rqs  = Reply.objects.get(id=qid)
                    qs.reply.add(rqs)
                    # qs.reply.add(rqs)
                    
                    return JsonResponse(data, status=200)

                    # print("datadata:::", rqs.author,rqs.id, rqs.to)

                    # data= {
                    #     "author":rqs.author.username,
                    #     "comment":rqs.comment,
                    #     "id":rqs.id
                    # }
                    # return JsonResponse({  "author":rqs.author.username,
                    #     "comment":rqs.comment,
                    #     "reply_id":rqs.id, "parent_id":comment_id, "pic":rqs.author.user_picture.url})
                return JsonResponse({"error":"error"})

            elif type=="reply-reply":
                reply_id= query.get("reply_id", None)
                comment= query.get("comment", None)
                parentComment= query.get("parent_id", None)
                to_id = query.get("to_id", None)


                # post_id= query.get("post_id", None)
                print("reply_id::::", reply_id)
                print("comment::::", comment)


                if comment and reply_id:
                    qs = PostComment.objects.get(id=parentComment)

                    author_id= user.id
                    to_id= reply_id
                    postcomment_id = qs.id
                    # comment= 
                    mydata ={
                        "author_id":author_id,
                        "postcomment_id":postcomment_id,
                        "comment":comment,
                        "to_id":to_id
                    }
                    data1 = self.serializer_class(data= mydata)
                    data1.is_valid(raise_exception=True)
                    data1.save()
                    data=data1.data
                    print("data1::",data)
                    qid= data.get("id")
                    print("qid::",id)

                    rqs  = Reply.objects.get(id=qid)
                    qs.reply.add(rqs)
                    # rqs  = Reply.objects.create(author=user, comment=comment, postcomment=qs, to=qs1)
                    # qs.reply.add(rqs)
                    # data = self.serializer_class(data= request.data)
                    # data.is_valid(raise_exception=True)
                    # print("datadata:::", rqs.author,rqs.id, rqs.to)
                    # data= {
                    #     "author":rqs.author,
                    #     "comment":rqs.comment,
                    #     "to":rqs.to.author.username,
                    #     "to_id": rqs.rqs.to.id,
                    #     "id":rqs.id
                    # }
                    return JsonResponse(data, status=200)
                return JsonResponse({"error":"error"})


        except Exception as e:
            print("ReplyView Error1:::", e)
            # return self.
    # queryset = Message.objects.select_related(
    #     "sender", "receiver").prefetch_related("message_attachments")
    # blogs =self.queryset.annotate(comment_count=Count("blog_comments")).order_by("-comment_count")[:5]
