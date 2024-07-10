from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('profile_list/', views.profile_list, name="profile_list"),
    path('profile/<str:pk>/', views.profile, name="profile"),
    path("profile/followers/<int:pk>/", views.followers, name="followers"),
    path("profile/following/<int:pk>/", views.following, name="following"),
    
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('register/', views.register_user, name="register"),
    path('update_user/', views.update_user, name="update_user"),
    path('tweet_like/<int:pk>/', views.tweet_like, name="tweet_like"),
    path("tweet_share/<int:pk>/", views.tweet_share, name="tweet_share"),
    path("unfollow/<int:pk>/", views.unfollow_user, name="unfollow"),
    path("follow/<int:pk>/", views.follow_user, name="follow"),
    path("delete_post/<int:pk>/", views.deletepost, name="deletepost"),
    path("edit_post/<int:pk>/", views.editpost, name="editpost"),
    path('search/', views.search, name='search'),
    path("search_user/", views.searchuser, name="searchuser"),
    
     
]
