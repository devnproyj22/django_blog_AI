from django.contrib import admin
from .models import SportType, SportMilestone, SportSession, Category, Tag, Post, Comment, MilestoneProgress

@admin.register(SportType)
class SportTypeAdmin(admin.ModelAdmin):
    list_display = ('sport_type',)
    search_fields = ('sport_type',)

@admin.register(SportMilestone)
class SportMilestoneAdmin(admin.ModelAdmin):
    list_display = ('sport_milestone', 'sport_type')
    list_filter = ('sport_type',)
    search_fields = ('sport_milestone',)

@admin.register(SportSession)
class SportSessionAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'user', 'exercise_at', 'exercise_loc', 'exercise_dur')
    list_filter = ('user', 'exercise_at')
    search_fields = ('user__username', 'exercise_loc')
    date_hierarchy = 'exercise_at'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('post_id', 'post_title', 'post_user', 'post_sport_type', 'post_sport_milestone', 'category', 'created_at')
    list_filter = ('post_sport_type', 'post_sport_milestone', 'category', 'created_at')
    search_fields = ('post_title', 'post_content', 'post_user__username')
    date_hierarchy = 'created_at'
    filter_horizontal = ('tags',)
    raw_id_fields = ('post_user', 'post_session')
    inlines = [CommentInline]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment_id', 'comment_user', 'comment_post', 'created_at')
    list_filter = ('comment_user', 'created_at')
    search_fields = ('comment_content', 'comment_user__username', 'comment_post__post_title')
    date_hierarchy = 'created_at'

@admin.register(MilestoneProgress)
class MilestoneProgressAdmin(admin.ModelAdmin):
    list_display = ('m_progress_id', 'pg_sport_type', 'pg_sport_milestone', 'post_count')
    list_filter = ('pg_sport_type', 'pg_sport_milestone')
    search_fields = ('pg_sport_type__sport_type', 'pg_sport_milestone__sport_milestone')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('pg_sport_type', 'pg_sport_milestone')