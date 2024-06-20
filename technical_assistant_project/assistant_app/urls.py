from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('memo/',  views.memo, name='memo'),
    path('memo_file/',  views.memo_file, name='memo_file'),
    path('support/',  views.support, name='support'),
    path('git_issues/',  views.git_issues, name='git_issues'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"), 
    path("issues_list/", views.Issues_List.as_view(), name="issues_list"),
]