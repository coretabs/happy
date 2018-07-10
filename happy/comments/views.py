from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
from fun.permissions import IsOwnerOrReadOnly


from .models import Comment, Reply

from .serializers import CommentSerializer, ReplySerializer
# Create your views here.


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['get'])
    def replies(self, request, pk=None):
        replies = Reply.objects.filter(parent_id=pk)
        serializer = ReplySerializer(replies, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def like(self, request , pk=None):
        comment = Comment.objects.get(pk=pk)
        if comment.likes.filter(id=request.user.id).exists():
            comment.likes.remove(request.user)
            return Response("Like has been removed")
        else: 
            if comment.dislikes.filter(id=request.user.id).exists():
                comment.dislikes.remove(request.user)
            comment.likes.add(request.user)
            return Response("Like has been added")

    @action(detail=True, methods= ["get"])
    def dislike(self, request, pk=None):
        comment = Comment.objects.get(pk=pk)
        if comment.dislikes.filter(id=request.user.id).exists():
            comment.dislikes.remove(request.user)
            return Response("Dislike has been removed")
        else: 
            if comment.likes.filter(id=request.user.id).exists():
                comment.likes.remove(request.user)
            comment.dislikes.add(request.user)
            return Response("Dislike has been added")



class ReplyViewSet(viewsets.ModelViewSet):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['get'])
    def like(self, request , pk=None):
        reply = Reply.objects.get(pk=pk)
        if reply.likes.filter(id=request.user.id).exists():
            reply.likes.remove(request.user)
            return Response("Like has been removed")
        else: 
            if reply.dislikes.filter(id=request.user.id).exists():
                reply.dislikes.remove(request.user)
            reply.likes.add(request.user)
            return Response("Like has been added")

    @action(detail=True, methods= ["get"])
    def dislike(self, request, pk=None):
        reply = Reply.objects.get(pk=pk)
        if reply.dislikes.filter(id=request.user.id).exists():
            reply.dislikes.remove(request.user)
            return Response("Dislike has been removed")
        else: 
            if reply.likes.filter(id=request.user.id).exists():
                reply.likes.remove(request.user)
            reply.dislikes.add(request.user)
            return Response("Dislike has been added")
