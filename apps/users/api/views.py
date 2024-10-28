from rest_framework import generics
from rest_framework import views
from .serializers import (
    UserListSerializer,
    UserFollowSerializer,
    UserDetailSerializer,
)
from ..models import User, Follow
from django.db.models import Count
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
)
from apps.core.permissions import (
    IsUserOwnerOrReadOnly,
    ReadOnly,
)
from rest_framework.filters import SearchFilter
from apps.core.paginations import SmallResultPagination
from apps.blog.models import Post
from apps.blog.api.serializers import PostListSerializer


class UserListView(generics.ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = [AllowAny, ReadOnly]
    pagination_class = SmallResultPagination
    filter_backends = [SearchFilter]
    search_fields = ["email", "last_name"]

    def get_queryset(self):
        return User.objects.all().select_related("profile").annotate(
            followers_count = Count("followers", distinct=True),
            followings_count = Count("followings", distinct=True)
        )


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [IsUserOwnerOrReadOnly|IsAdminUser]

    def get_queryset(self):
        return User.objects.all().select_related("profile").annotate(
            followers_count = Count("followers", distinct=True),
            followings_count = Count("followings", distinct=True)
        )


class UserFollowersView(generics.ListAPIView):
    serializer_class = UserFollowSerializer
    permission_classes = [AllowAny, ReadOnly]
    pagination_class = SmallResultPagination

    def get_queryset(self):
        return User.objects.all().filter(followings__following=self.kwargs["pk"])


class UserFollowingsView(generics.ListAPIView):
    serializer_class = UserFollowSerializer
    permission_classes = [AllowAny, ReadOnly]
    pagination_class = SmallResultPagination

    def get_queryset(self):
        return User.objects.all().filter(followers__follower=self.kwargs["pk"])


class FollowUnfollowView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        try:
            Follow.objects.create(follower=request.user, following_id=pk)
            return Response(data={"detail": _("followed successfully")}, status=status.HTTP_201_CREATED)
        except IntegrityError as error:
            if "UNIQUE constraint" in str(error):
                return Response({"detail": _("you are already following this user")}, status=status.HTTP_400_BAD_REQUEST)
            elif "CHECK constraint" in str(error):
                return Response({"detail": _("you cannot follow your self")}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({"detail": str(error)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        deleted, objs = Follow.objects.filter(follower=request.user, following_id=pk).delete()
        if deleted:
            return Response({"detail": _("unfollowed successfully")}, status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": _("you are not following this user")}, status=status.HTTP_400_BAD_REQUEST)


class RemoveFollowerView(views.APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, *args, **kwargs):
        deleted, objs = Follow.objects.filter(follower=pk, following_id=request.user).delete()
        if deleted:
            return Response({"detail": _("follower removed successfully")}, status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": _("this user not following you")}, status=status.HTTP_400_BAD_REQUEST)


class LikedPostsView(generics.ListAPIView):
    serializer_class = PostListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = SmallResultPagination

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(likes=user).select_related("author")
