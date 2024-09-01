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
    path('<int:post_id>/', PostDetailView.as_view(), name='post_detail'),
    path('new/', PostCreateView.as_view(), name='post_create'),
    path('<int:post_id>/update/', PostUpdateView.as_view(), name='post_update'),
    path('<int:post_id>/delete/', PostDeleteView.as_view(), name='post_delete'),
]
comment_crud = [
    path('<int:post_id>/comments/new/', PostCommentCreateView.as_view(), name='comment_create'),
    path('<int:post_id>/comments/<int:comment_id>/update/', PostCommentUpdateView.as_view(), name='comment_update'),
    path('<int:post_id>/comments/<int:comment_id>/delete/', PostCommentDeleteView.as_view(), name='comment_delete'),
	
]
category_tag = [
    path('category/<slug:slug>/', CategoryPostListView.as_view(), name='category_posts'),
    path('tags/slug:slug>/', TagPostListView.as_view(), name='tag_posts'),
]

urlpatterns = post_crud + comment_crud + category_tag