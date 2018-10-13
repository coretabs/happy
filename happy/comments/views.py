from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Comment, Reply
from posts.pagination import CommentsPageNumberPagination, PostsPageNumberPagination


from .serializers import (CommentSerializer,
                          ReplySerializer, CommentLikesSerializer)


class CommentViewSet2(viewsets.ModelViewSet):
    queryset = Comment.objects.filter()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)
    pagination_class = PostsPageNumberPagination

    def list(self, request, post_pk=None):
        queryset = Comment.objects.filter(parent_id=post_pk)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={"request":request})
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True, context={"request":request})
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
        serializer = CommentSerializer(comment, context={"request":request})
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
        if not request.user.is_authenticated:
            return Response("Authentication credentials were not provided.")
        else:
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
        if not request.user.is_authenticated:
            return Response("Authentication credentials were not provided.")
        else:
            comment = Comment.objects.get(pk=pk)
            if comment.dislikes.filter(id=request.user.id).exists():
                comment.dislikes.remove(request.user)
                return Response("Dislike has been removed")
            else: 
                if comment.likes.filter(id=request.user.id).exists():
                    comment.likes.remove(request.user)
                comment.dislikes.add(request.user)
                return Response("Dislike has been added")
    
    @action(detail=True, methods=['get'])
    def likes(self, request, pk=None, post_pk=None):
        likes = Comment.objects.get(pk=pk).likes.all()
        serializer = CommentLikesSerializer(likes, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def dislikes(self, request, pk=None, post_pk=None):
        dislikes = Comment.objects.get(pk=pk).dislikes.all()
        serializer = CommentLikesSerializer(dislikes, many=True)
        return Response(serializer.data)
    

class ReplyViewSet2(viewsets.ModelViewSet):
    queryset = Reply.objects.filter()
    serializer_class = ReplySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)
    pagination_class = CommentsPageNumberPagination

    def list(self, request, post_pk=None, comment_pk=None):
        queryset = Reply.objects.filter(parent_id=comment_pk)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={"request":request})
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True, context={"request":request})
        return Response(serializer.data)
        
        #queryset = Comment.objects.filter(pk=comment_pk)
        #serializer = CommentSerializer(queryset, many=True, context={"request":request})
        #return Response(serializer.data)
    
    def create(self, request, post_pk=None, comment_pk=None):
        serializer = ReplySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=self.request.user, parent_id=comment_pk)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None, post_pk=None, comment_pk=None):
        queryset =  Reply.objects.filter(pk=pk, parent__parent=post_pk, parent_id=comment_pk)
        reply =  get_object_or_404(queryset, pk=pk)
        serializer = ReplySerializer(reply, context={'request': request})
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
        if not request.user.is_authenticated:
            return Response("Authentication credentials were not provided.")
        else:
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
        if not request.user.is_authenticated:
            return Response("Authentication credentials were not provided.")
        else:
            reply = Reply.objects.get(pk=pk)
            if reply.dislikes.filter(id=request.user.id).exists():
                reply.dislikes.remove(request.user)
                return Response("Dislike has been removed")
            else: 
                if reply.likes.filter(id=request.user.id).exists():
                    reply.likes.remove(request.user)
                reply.dislikes.add(request.user)
                return Response("Dislike has been added")
        

    @action(detail=True, methods=['get'])
    def likes(self, request, pk=None, post_pk=None, comment_pk=None):
        likes = Reply.objects.get(pk=pk).likes.all()
        serializer = CommentLikesSerializer(likes, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def dislikes(self, request, pk=None, post_pk=None, comment_pk=None):
        dislikes = Reply.objects.get(pk=pk).dislikes.all()
        serializer = CommentLikesSerializer(dislikes, many=True)
        return Response(serializer.data)