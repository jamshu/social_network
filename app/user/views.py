"""
Views for the user API.
"""
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.decorators import action
from .models import FriendRequest,Friend
from .throttling import FriendRequestThrottle
from .pagination import UserSearchPagination
from rest_framework import status
from rest_framework.response import Response
from rest_framework import filters
from django.db.models import Q
from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
    FriendRequestSerializer,
)


class SignupView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer


class LoginView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user


class UserSearchView(generics.ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'email']
    pagination_class = UserSearchPagination

    # def get_queryset(self):
    #     search_keyword = self.request.query_params.get("search_keyword", None)
    #     if search_keyword:
    #         return get_user_model().objects.filter(Q(email__iexact=search_keyword) | Q(first_name__icontains=search_keyword) | Q(last_name__icontains=search_keyword))
    #     else:
    #         return get_user_model().objects.none()


class ListFriendsView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        friends = user.user_friends.all().values_list('to_user', flat=True)
        return get_user_model().objects.filter(id__in=friends)


class ListPendingFriendRequestsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return FriendRequest.objects.filter(Q(to_user=user))


class SendFriendRequestView(generics.CreateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [FriendRequestThrottle]

    def perform_create(self, serializer):
        try:
            serializer.save(from_user=self.request.user)
        except Exception as e:
            return Response({"Message": str(e)}, status=status.HTTP_400_BAD_REQUEST) 


class AcceptFriendRequestView(generics.UpdateAPIView):
    queryset = FriendRequest.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FriendRequestSerializer

    def patch(self, request, *args, **kwargs):
        try:
            friend_request = self.get_object()
            if friend_request.to_user == request.user:
                print("printing friend requst",friend_request.to_user, request.user)
                Friend.objects.create(from_user=friend_request.from_user, to_user=friend_request.to_user)
                Friend.objects.create(from_user=friend_request.to_user, to_user=friend_request.from_user)
                friend_request.delete()
                return Response({"Message": "Friend Request Accepted"}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"Message": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"Message": str(e)}, status=status.HTTP_400_BAD_REQUEST)            


class RejectFriendRequestView(generics.DestroyAPIView):
    queryset = FriendRequest.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FriendRequestSerializer

    def delete(self, request, *args, **kwargs):
        friend_request = self.get_object()
        if friend_request.to_user == request.user:
            friend_request.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
