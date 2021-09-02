from django.shortcuts import render
from .serializers import ChatListSerializer
from .models import ChatList
from rest_framework.viewsets import ModelViewSet
from user_controller.models import CustomUser
from rest_framework.generics import ListAPIView
from django.http import JsonResponse
from litty.custom_methods import IsAuthenticatedCustom
from rest_framework.views import APIView

# Create your views here.
class ChatListView(ModelViewSet):
    queryset = ChatList.objects.all()

    permission_classes = (IsAuthenticatedCustom,)
    # pagination_class = PaginationInterface
    serializer_class = ChatListSerializer
    lookup_field = "id"

    def get_queryset(self):
        try:
            self.queryset = ChatList.objects.all()
            query = self.request.query_params.dict()
            user= self.request.user
            if user:
                # print("keyword::::", username)
                user  = CustomUser.objects.get(id=user.id)
                print("user::::", user)
                print("username::::", user.username)

                query_data = self.queryset.filter(user = user)
                return query_data
            return None
        except Exception as e:
            print("ChatList Error:::", e)
            # return self.
            