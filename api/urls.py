from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import PostViewSet, APIComment, APICommentDetail, FollowViewSet, \
    GroupViewSet

router_post = DefaultRouter()
router_post.register(r'posts', PostViewSet)
router_post.register(r'follow', FollowViewSet)
router_post.register(r'group', GroupViewSet)

urlpatterns = [
    path('', include(router_post.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('posts/<int:post_id>/comments/', APIComment.as_view()),
    path(
        'posts/<int:post_id>/comments/<int:comment_id>/',
        APICommentDetail.as_view()
    ),
]
