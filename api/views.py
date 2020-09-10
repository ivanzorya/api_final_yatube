from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Post, Comment, Follow, Group
from .permissions import IsOwnerOrReadOnly
from .serializers import PostSerializer, CommentSerializer, FollowSerializer, \
    GroupSerializer, FollowSlugSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group', ]

    def create(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]

    def list(self, request, post_id):
        queryset = Comment.objects.filter(post=post_id)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, post_id):
        serializer = CommentSerializer(data=request.data)
        post = get_object_or_404(Post, pk=post_id)
        if serializer.is_valid():
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSlugSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'post']
    filter_backends = [SearchFilter]
    search_fields = ['=user__username', '=following__username']

    def create(self, request):
        following_name = self.request.data.get('following', None)
        if following_name is not None:
            following = get_object_or_404(User, username=following_name)
            user = get_object_or_404(User, username=request.user)
            data = {'user': user.pk, 'following': following.pk}
            serializer = FollowSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                data = {
                    'user': user.username,
                    'following': following.username
                }
                return Response(data, status=201)
            return Response(serializer.errors, status=400)
        return Response(
            {'Вы не передали имя пользователя для фильтрации по подписчикам'},
            status=400
        )


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'post']


