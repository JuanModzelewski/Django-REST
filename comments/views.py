from rest_framework import permissions, generics
from .models import Comment
from .serializers import CommentSerializer, CommentDetailSerializer
from drf_api.permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend


class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    queryset = Comment.objects.all()

    filter_backends = [
        DjangoFilterBackend,
        ]
    
    filterset_fields = [
        'post',
        
        ]
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a comment instance
    """
    serializer_class = CommentDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Comment.objects.all()
