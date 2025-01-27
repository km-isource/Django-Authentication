from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path("logout/", views.LogOut, name="logout"),
    path('home', views.home, name='home'),
    path('sign-up/', views.sign_up, name='sign_up'),
    path(
        "change-password/",
        auth_views.PasswordChangeView.as_view(template_name="registration/change-password.html"),
    ),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('create-post/', views.create_post, name='create_post')
]
