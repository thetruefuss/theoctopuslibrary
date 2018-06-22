from accounts.api.serializers import UserPublicSerializer
from pinax.messages.models import Message, Thread
from rest_framework import serializers


class ThreadListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='messages-api:thread_retrieve',
        lookup_field='pk'
    )
    latest_message_content = serializers.SerializerMethodField()
    is_unread = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = (
            'url', 'subject', 'users', 'latest_message_content', 'is_unread',
        )

    def get_latest_message_content(self, obj):
        return obj.latest_message.content

    def get_is_unread(self, obj):
        request = self.context.get('request')
        return bool(obj.userthread_set.filter(user=request.user, unread=True))


class MessageSerializer(serializers.ModelSerializer):
    sender = UserPublicSerializer(read_only=True)

    class Meta:
        model = Message
        fields = (
            'content', 'sender', 'sent_at'
        )


class ThreadRetrieveSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True)

    class Meta:
        model = Thread
        fields = (
            'id', 'messages',
        )
