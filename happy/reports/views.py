from rest_framework import viewsets
from django.db.models import Count
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import action

from .models import PostReport
from django.db.models import OuterRef, Subquery, Count, Min


from .serializers import PostReportSerializer

class PostReportViewSet(viewsets.ModelViewSet):
    queryset = PostReport.objects.all()
    serializer_class =  PostReportSerializer
    

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True, context={"request":request})
        return Response(serializer.data)
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data, context={"request":request})
        if serializer.is_valid():
            serializer.save(reporter=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = self.filter_queryset(self.get_queryset())
        report =  get_object_or_404(queryset, pk=pk)

        serializer = self.get_serializer(report, context={"request":request})
        return Response(serializer.data)