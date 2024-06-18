from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('memo/',  views.memo, name='memo'),
    path('memo_file/',  views.memo_file, name='memo_file'),
    path('support/',  views.support, name='support'),
]