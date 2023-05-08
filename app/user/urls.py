"""
URL mappings for the user API.
"""
from django.urls import path

from user import views


app_name = 'user'

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='create'),
    path('login/', views.LoginView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('search/', views.UserSearchView.as_view(), name='user_search'),
    path('send-friend-request/', views.SendFriendRequestView.as_view(), name='send_friend_request'),
    path('accept-friend-request/<int:pk>/', views.AcceptFriendRequestView.as_view(), name='accept_friend_request'),
    path('reject-friend-request/<int:pk>/', views.RejectFriendRequestView.as_view(), name='reject_friend_request'),
    path('list-friends/', views.ListFriendsView.as_view(), name='list_friends'),
    path('list-pending-friend-requests/', views.ListPendingFriendRequestsView.as_view(), name='list_pending_friend_requests'),
]
