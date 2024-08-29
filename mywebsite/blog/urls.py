from django.urls import path
from .views import (
    PostListView, 
    PostDetailView,
    PostCreateView,
    PostUpdateView, 
    PostDeleteView,
    PostCommentCreateView,
    PostCommentUpdateView,
    PostCommentDeleteView,
    CategoryPostListView,
    TagPostListView,
)

app_name='blog'                           # 'blog/'로 시작하는 URL 패턴

post_crud = [
    path('', PostListView.as_view(), name='post_list'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('new/', PostCreateView.as_view(), name='post_create'),
    path('<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
]
comment_crud = [
    path('<int:pk>/comments/new/', PostCommentCreateView.as_view(), name='comment_create'),
    path('<int:pk>/comments/<int:comment_pk>/update/', PostCommentUpdateView.as_view(), name='comment_update'),
    path('<int:pk>/comments/<int:comment_pk>/delete/', PostCommentDeleteView.as_view(), name='comment_delete'),
	
]
category_tag = [
    path('category/<str:slug>/', CategoryPostListView.as_view(), name='category_page'),
    path('tag/<str:slug>/', TagPostListView.as_view(), name='tag_page'),
]

urlpatterns = post_crud + comment_crud + category_tag