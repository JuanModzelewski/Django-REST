from rest_framework import generics
from .models import Like
from .serializers import LikeSerializer
from drf_api.permissions import IsOwnerOrReadOnly

class LikeList(generics.ListCreateAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = LikeSerializer
    queryset = Like.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LikeDetail(generics.RetrieveDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = LikeSerializer
    queryset = Like.objects.all()