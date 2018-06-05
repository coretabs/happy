from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


from .models import Comment, Reply

from .serializers import CommentSerializer, ReplySerializer
# Create your views here.


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    @action(detail=True, methods=['get'])
    def replies(self, request, pk=None):
        replies = Reply.objects.filter(parent_id=pk)
        serializer = ReplySerializer(replies, many=True)
        return Response(serializer.data)


class ReplyViewSet(viewsets.ModelViewSet):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
