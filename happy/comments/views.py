from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly
from rest_framework import status
from django.shortcuts import get_object_or_404

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
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

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


class CommentViewSet2(viewsets.ViewSet):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def list(self, request, post_pk=None):
        queryset = Comment.objects.filter(parent_id=post_pk)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, post_pk=None):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=self.request.user, parent_id=post_pk)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None, post_pk=None):
        queryset =  Comment.objects.filter()
        comment =  get_object_or_404(queryset, pk=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
    
    def update(self, request, pk=None, post_pk=None):
        comment =  Comment.objects.get(pk=pk)
        serializer = CommentSerializer(data=request.data, instance=comment)
        if serializer.is_valid():
            comment = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None, post_pk=None):
        try:
            comment =  Comment.objects.get(pk=pk)
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['get'])
    def like(self, request , pk=None, post_pk=None):
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
    def dislike(self, request, pk=None, post_pk=None):
        comment = Comment.objects.get(pk=pk)
        if comment.dislikes.filter(id=request.user.id).exists():
            comment.dislikes.remove(request.user)
            return Response("Dislike has been removed")
        else: 
            if comment.likes.filter(id=request.user.id).exists():
                comment.likes.remove(request.user)
            comment.dislikes.add(request.user)
            return Response("Dislike has been added")
    

class ReplyViewSet2(viewsets.ViewSet):
    serializer_class = ReplySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def list(self, request, post_pk=None, comment_pk=None):
        queryset = Comment.objects.filter(pk=comment_pk)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, post_pk=None, comment_pk=None):
        serializer = ReplySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=self.request.user, parent_id=comment_pk)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None, post_pk=None, comment_pk=None):
        queryset =  Reply.objects.filter(pk=pk, parent__parent=post_pk, parent_id=comment_pk)
        reply =  get_object_or_404(queryset, pk=pk)
        serializer = ReplySerializer(reply)
        return Response(serializer.data)
    
    def update(self, request, pk=None, post_pk=None, comment_pk=None):
        reply =  Reply.objects.get(pk=pk)
        serializer = ReplySerializer(data=request.data, instance=reply)
        if serializer.is_valid():
            reply = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None, post_pk=None, comment_pk=None):
        try:
            reply =  Reply.objects.get(pk=pk)
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        reply.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['get'])
    def like(self, request , pk=None, post_pk=None, comment_pk=None):
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
    def dislike(self, request, pk=None, post_pk=None, comment_pk=None):
        reply = Reply.objects.get(pk=pk)
        if reply.dislikes.filter(id=request.user.id).exists():
            reply.dislikes.remove(request.user)
            return Response("Dislike has been removed")
        else: 
            if reply.likes.filter(id=request.user.id).exists():
                reply.likes.remove(request.user)
            reply.dislikes.add(request.user)
            return Response("Dislike has been added")