from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.index, name='index'),
    path('memo/',  views.memo, name='memo'),
    path('memo_file/',  views.memo_file, name='memo_file'),
    path('support/',  views.support, name='support'),
    path('git_issues/',  views.git_issues, name='git_issues'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"), 
    path("issues_list/", views.Issues_List.as_view(), name="issues_list"),
    path('create_group/', views.create_group, name='create_group'),
    path('edit_group/', views.edit_group, name='edit_group'),
    path('group_list/', views.group_list, name='group_list'),
    path('group_detail/<int:group_id>/', views.group_detail, name='group_detail'),
    path('add_group_item/<int:group_id>/', views.add_group_item, name='add_group_item'),
    path('add_member/<int:group_id>/', views.add_member, name='add_member'),
    path('remove_member/<int:group_id>/', views.remove_member, name='remove_member'),
    path('login_team/', views.login_team, name='login_team'),
]