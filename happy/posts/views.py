# from django.shortcuts import render
from .permissions import IsOwnerOrReadOnly
from rest_framework import viewsets
#from django.utils import timezone
#from datetime import timedelta
#from django.db.models import Case , When 
from django.db.models import Count
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status
from rest_framework.decorators import action

from .models import Post
from .filters import PostFilter
from .pagination import PostsLimitOffsetPagination, PostsPageNumberPagination
from .serializers import (PostSerializer, SinglePostSerializer, 
                          PostLikesSerializer, PostReportListSerializer)

from comments.models import Comment, Reply
from comments.serializers import CommentSerializer, ReplySerializer
from reports.serializers import PostReportSerializer
from reports.models import PostReport


class PostViewSet2(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class =  PostSerializer

    def get_serializer_class(self):
        if self.action == 'report':
            return PostReportSerializer
        return super(PostViewSet2, self).get_serializer_class()
    
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    pagination_class = PostsPageNumberPagination
    filterset_class = PostFilter

    def get_queryset(self):
        #now = timezone.now()
        #date_day = timezone.now() - timedelta(hours=24) 
        data = Post.objects.annotate(
            score = (Count("likes") + Count("post_comments")) - Count("dislikes")
            ).order_by("-score","-created")
        return data

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={"request":request})
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True, context={"request":request})
        return Response(serializer.data)
    
    def create(self, request):
        serializer = PostSerializer(data=request.data, context={"request":request})
        if serializer.is_valid():
            serializer.save(author=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        queryset = self.filter_queryset(self.get_queryset())
        post =  get_object_or_404(queryset, pk=pk)
        serializer = SinglePostSerializer(post,context={"request":request})
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        queryset = self.filter_queryset(self.get_queryset())
        post =  get_object_or_404(queryset, pk=pk)
        serializer = PostSerializer(data=request.data, instance=post)
        if serializer.is_valid():
            post = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            post =  get_object_or_404(queryset, pk=pk)
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['get'])
    def like(self, request , pk=None):
        if not request.user.is_authenticated:
            return Response("Authentication credentials were not provided.")
        else:
            post = Post.objects.get(pk=pk)
            if post.likes.filter(id=request.user.id).exists():
                post.likes.remove(request.user)
                return Response("Like has been removed")
            else: 
                if post.dislikes.filter(id=request.user.id).exists():
                    post.dislikes.remove(request.user)
                post.likes.add(request.user)
                return Response("Like has been added")

    @action(detail=True, methods= ["get"])
    def dislike(self, request, pk=None):
            if not request.user.is_authenticated:
                return Response("Authentication credentials were not provided.")
            else:
                post = Post.objects.get(pk=pk)
                if post.dislikes.filter(id=request.user.id).exists():
                    post.dislikes.remove(request.user)
                    return Response("Dislike has been removed")
                else: 
                    if post.likes.filter(id=request.user.id).exists():
                        post.likes.remove(request.user)
                    post.dislikes.add(request.user)
                    return Response("Dislike has been added")

    @action(detail=True, methods=['get'])
    def likes(self, request , pk=None):
        likes = Post.objects.get(pk=pk).likes.all()
        serializer = PostLikesSerializer(likes, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def dislikes(self, request , pk=None):
        dislikes = Post.objects.get(pk=pk).dislikes.all()
        serializer = PostLikesSerializer(dislikes, many=True)
        return Response(serializer.data)

    @action(detail=True, methods= ["post"],
            permission_classes=(IsAuthenticatedOrReadOnly,)
        )
    def report(self, request, pk=None):
        if not request.user.is_authenticated:
            return Response("Authentication credentials were not provided.")
        else:
            post = Post.objects.get(pk=pk)
            serializer = PostReportSerializer(data=request.data)
            if serializer.is_valid():
                #serializer.save(post_id=post.id)
                serializer.save(reporter=self.request.user, post_id=pk)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostReportViewSet(viewsets.ViewSet):
    queryset = Post.objects.filter()

    def list(self, request):
        queryset = Post.objects.filter(reports__isnull=False
               ).annotate(reports_count=Count('reports')
               ).order_by('-reports_count')
        serializer = PostReportListSerializer(queryset, many=True, context={"request":request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset,pk=pk)
        reports = post.reports.all()
        serializer = PostReportSerializer(reports, many=True, context={"request":request})
        return Response(serializer.data)