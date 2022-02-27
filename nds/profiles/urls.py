from django.urls import path
from .views import (
    my_profile_view,
    invites_received_view,
    profiles_list_view,
    invite_profiles_list_view,
    ProfileDetailView,
    ProfileListView,
    send_invitation,
    remove_from_friends,
    accept_invitation,
    reject_invitation,
)

app_name = 'profiles'

urlpatterns = [
    path('', ProfileListView.as_view(), name='all-profiles-view'),
    path('myprofile/', my_profile_view, name='my-profile-view'), # http://127.0.0.1:8000/profiles/myprofile
    path('my_invites/', invites_received_view, name='my-invites-view'),
    path('to_invite/', invite_profiles_list_view, name='invite-profiles-view'),
    path('send_invite/', send_invitation, name='send-invite'),
    path('remove_friend/', remove_from_friends, name='remove-friend'),
    path('<slug>/', ProfileDetailView.as_view(), name='profile-detail-view'),
    path('my_invites/accept/', accept_invitation, name='accept-invite'),
    path('my_invites/reject/', reject_invitation, name='reject-invite'),
]
