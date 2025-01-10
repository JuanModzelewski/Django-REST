from rest_framework import permissions, generics, filters #, status,
# from rest_framework.response import Response
# from rest_framework.views import APIView
from .models import Post
from .serializers import PostSerializer
# from django.http import Http404
from drf_api.permissions import IsOwnerOrReadOnly
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend

"""
class PostList(APIView):
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(
            posts, many=True, context={'request': request}
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )
"""

class PostList(generics.ListCreateAPIView):
    """
    List posts or create a post if logged in
    The perform_create method associates the post with the logged in user.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.annotate(
        comments_count=Count('comment', distinct=True),
        likes_count=Count('likes', distinct=True)
    ).order_by('-created_at')
    
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend
        ]

    ordering_fields = [
        'likes_count',
        'comments_count',
        'created_at'
        ]
    
    search_fields = [
        'owner__username',
        'title',
        ]
    
    filterset_fields = [
        'owner__following__owner__profile', 
        'likes__owner__profile',
        'owner__profile',
        ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    

"""
class PostDetail(APIView):
    
    ### Retrieve, update or delete a profile instance
    
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    def get_object(self, pk):
        try:
            posts = Post.objects.get(pk=pk)
            self.check_object_permissions(self.request, posts)
            return posts
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        posts = self.get_object(pk)
        serializer = PostSerializer(posts, context={'request': request})
        return Response(serializer.data)
    
    def put(self, request, pk):
        posts = self.get_object(pk)
        serializer = PostSerializer(posts, data=request.data, context={'request': request})
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        posts = self.get_object(pk)
        posts.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
"""

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a post and edit or delete it if you own it.
    """
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.annotate(
        comments_count=Count('comment', distinct=True),
        likes_count=Count('likes', distinct=True)
    ).order_by('-created_at')