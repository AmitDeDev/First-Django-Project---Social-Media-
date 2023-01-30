from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('feed/', views.feed, name='feed'),
    path('feed/friendsposts/', views.friends_feed, name='friendsposts'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('signup/', views.signup_user, name='signup'),
    path('profile/<str:username>/',
         views.profile_username, name='profile_username'),
    path('profile/<str:username>/edit/', views.edit_profile, name='editprofile'),
    path('profile/<str:username>/remove',
         views.remove_profile, name='remove_profile'),
    path('post/<str:username>/add', views.new_post, name='new_post'),
    # need to change test in post edit -> postID
    path('post/<str:id>/spesific', views.post_spesific, name='post_spesific'),
    # need to change test in post edit -> postID
    path('post/<str:id>/edit', views.edit_post, name='edit_post'),
    path('post/<str:id>/remove', views.remove_post, name='remove_post'),
    path('following/', views.nav_following, name='nav_following'),
    path('like/<str:id>/', views.addRemoveLike, name='likes'),
    path('newfollowers/', views.new_followers, name='new_followers'),
    path('addcomment/<str:id>/', views.addComment, name='addcomment'),
    path('removecomment/<str:id>/', views.remove_Comment, name='remove_Comment'),
    path('editcomment<str:id>/edit', views.edit_comment, name='edit_comment'),
    path('addfriend/<str:username>', views.addFriend, name='addfriend'),
    path('tutorial/', views.tutorial, name='tutorial'),
    path('comingsoon/', views.comingsoon, name='comingsoon'),
    path('search/', views.search, name='search')
]
