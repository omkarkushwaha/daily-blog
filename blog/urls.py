from django.urls import path
from . import views

urlpatterns = [

    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path("post/<int:pk>/", views.PostDetailView.as_view(), name="post_detail"),
    path("create/",views.CreatePostView.as_view(),name="create_post"),
    path("post/<int:pk>/edit/",views.UpdatePostView.as_view(),name="update_post"),
    path("post/<int:pk>/delete/",views.DeletePostView.as_view(),name="delete_post"),
    path("register/",views.register,name="register"),
    path("login/",views.user_login,name="login"),
    path("logout/",views.user_logout,name="logout"),
    path("profile/", views.profile, name="profile"),
    path("category/<int:id>/",views.category_posts,name="category_posts"),

]