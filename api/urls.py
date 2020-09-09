from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import PostViewSet, FollowViewSet, GroupViewSet, CommentViewSet

router_post = DefaultRouter()
router_post.register(r'posts', PostViewSet)
router_post.register(r'follow', FollowViewSet)
router_post.register(r'group', GroupViewSet)
router_post.register(r'posts/(?P<post_id>[^/.]+)/comments', CommentViewSet)

urlpatterns = [
    path('', include(router_post.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
