from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Comment, Category, Tag
from .forms import PostForm, CommentForm 
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.shortcuts import render
from django.views.generic import (
																	ListView, 
																	DetailView, 
																	CreateView, 
																	UpdateView, 
																	DeleteView,
																	)

def custom_404(request, exception):
    return render(request, 'blog/404.html', status=404)

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'post_list'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.select_related('post_user', 'post_sport_type', 'post_sport_milestone', 'category').prefetch_related('tags')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'
    
    def get_object(self, queryset=None):
        post_id = self.kwargs.get(self.pk_url_kwarg)
        return get_object_or_404(Post, pk=post_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        return context

class PostCreateView(CreateView):
    model = Post
    form_class = PostForm 
    template_name = 'blog/post_form.html' 
    
    def form_valid(self, form):
        form.instance.post_user = self.request.user if self.request.user.is_authenticated else None
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'post_id': self.object.post_id})

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    pk_url_kwarg = 'post_id'
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.post_user
    
    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'post_id': self.kwargs['post_id']})

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')
    pk_url_kwarg = 'post_id'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.post_user

class PostCommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        form.instance.comment_post_id = self.kwargs['post_id']
        form.instance.comment_user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'post_id': self.kwargs['post_id']})



class PostCommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.comment_user
    
    def get_object(self, queryset=None):
        return Comment.objects.get(comment_id=self.kwargs['comment_id'])
    
    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'post_id': self.kwargs['post_id']})

class PostCommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.comment_user
    
    def get_object(self, queryset=None):
        return Comment.objects.get(comment_id=self.kwargs['comment_id'])
    
    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'post_id': self.kwargs['post_id']})

class CategoryPostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        slug = self.kwargs['slug']
        category = get_object_or_404(Category, slug=slug)
        return Post.objects.filter(category=category).select_related(
            'post_user', 'post_sport_type', 'post_sport_milestone', 'category'
        ).prefetch_related('tags')


class TagPostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        slug = self.kwargs['slug']
        tag = get_object_or_404(Tag, slug=slug)
        return Post.objects.filter(tags=tag).select_related(
            'post_user', 'post_sport_type', 'post_sport_milestone', 'category'
        ).prefetch_related('tags') 