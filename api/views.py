from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post, Comment, Follow, Group
from .permissions import IsOwnerOrReadOnly
from .serializers import PostSerializer, CommentSerializer, FollowSerializer, \
    GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]

    def list(self, request):
        group_id = self.request.query_params.get('group', None)
        queryset = Post.objects.all()
        if group_id is not None:
            group = get_object_or_404(Group, pk=group_id)
            queryset = Post.objects.filter(group=group)
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class APIComment(APIView):
    def get(self, request, post_id):
        comments = Comment.objects.filter(post=post_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, post_id):
        serializer = CommentSerializer(data=request.data)
        post = get_object_or_404(Post, pk=post_id)
        if serializer.is_valid():
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class APICommentDetail(APIView):
    permission_classes = [IsOwnerOrReadOnly]

    def get(self, request, post_id, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def put(self, request, post_id, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)
        self.check_object_permissions(request, comment)
        serializer = CommentSerializer(comment, data=request.data)
        post = get_object_or_404(Post, pk=post_id)
        if serializer.is_valid():
            serializer.save(author=request.user,  post=post)
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def patch(self, request, post_id, comment_id):
        post = get_object_or_404(Post, pk=post_id)
        comment = get_object_or_404(Comment, pk=comment_id)
        self.check_object_permissions(request, comment)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request, post_id, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)
        self.check_object_permissions(request, comment)
        comment.delete()
        return Response(status=204)


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]

    def list(self, request):
        name = self.request.query_params.get('search', None)
        print(request.query_params)
        queryset = Follow.objects.all()
        if name is not None:
            queryset = Follow.objects.filter(
                Q(user__username=name) | Q(following__username=name)
            )
        serializer = FollowSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        following_name = self.request.data.get('following', None)
        if following_name is not None:
            following = get_object_or_404(User, username=following_name)
            user = get_object_or_404(User, username=request.user)
            if user == following:
                return Response(
                    {'Нельзя подписаться на самого себя'},
                    status=400
                )
            follow = Follow.objects.filter(user=user, following=following)
            if len(follow) > 0:
                return Response(
                    {'Вы уже подписаны на этого пользователя'},
                    status=400
                )
            serializer = FollowSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user, following=following)
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        return Response(
            {'Вы не передали имя пользователя для фильтрации по подписчикам'},
            status=400
        )


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]

