from django.contrib.auth.models import User

from pinax.messages.models import Message, Thread
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     RetrieveUpdateAPIView, UpdateAPIView)
from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ThreadListSerializer, ThreadRetrieveSerializer


class MessageCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data
        to_user = data.get('to_user')
        subject = data.get('subject')
        content = data.get('content')
        user_obj = User.objects.filter(id=to_user)
        if user_obj.count() == 1:
            Message.new_message(
                self.request.user, user_obj, subject, content
            )
            return Response({
                "to_user": to_user,
                "subject": subject,
                "content": content
            })
        return Response({"detail": "User does not exists."}, status=401)



class ReplyCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data
        thread = data.get('thread')
        content = data.get('content')
        thread_obj = Thread.objects.get(id=thread)
        if thread_obj:
            Message.new_reply(
                thread_obj, self.request.user, content
            )
            return Response({
                "content": content
            })
        return Response({"detail": "Thread does not exists."}, status=401)


class ThreadListAPIView(ListAPIView):
    serializer_class = ThreadListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        queryset_list = Thread.ordered(Thread.inbox(self.request.user))
        return queryset_list

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class ThreadRetrieveAPIView(RetrieveAPIView):
    queryset = Thread.objects.all()
    serializer_class = ThreadRetrieveSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'

    def get_queryset(self, *args, **kwargs):
        queryset_list = Thread.objects.filter(userthread__user=self.request.user).distinct()
        return queryset_list

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}
