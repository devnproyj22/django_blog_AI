from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from common.models import BaseModel

CustomUser = get_user_model()

class SportType(BaseModel):
    '''운동종목'''

    class SportTypeChoices(models.TextChoices):
        GOLF = 'GOLF', '골프'
        TENNIS = 'TENNIS', '테니스'
        PILATES = 'PILATES', '필라테스'
        JOGGING = 'JOGGING', '조깅'
        HIKING = 'HIKING', '등산'
        SWIMMING = 'SWIMMING', '수영'

    sport_id = models.AutoField(primary_key=True, verbose_name="운동 종목 ID")
    sport_type = models.CharField(max_length=100, choices=SportTypeChoices.choices, unique=True, verbose_name="운동 종목")

    def __str__(self):
        return f"{self.sport_type}"

    class Meta:
        verbose_name = "운동 종목"
        verbose_name_plural = "운동 종목들"
    

class SportMilestone(BaseModel):
    '''운동중간목표'''

    class SportMilestoneChoices(models.TextChoices):
        RECORD_IMPROVEMENT = 'RECORD_IMPROVEMENT', '기록단축'
        REPETITIONS_INCREASE = 'REPETITIONS_INCREASE', '반복 횟수 증가'
        DISTANCE_EXTENSION = 'DISTANCE_EXTENSION', '거리연장'
        SKILL_IMPROVEMENT = 'SKILL_IMPROVEMENT', '기술 향상'
        CONSISTENCY = 'CONSISTENCY', '일정 유지'
        STAMINA_IMPROVEMENT = 'STAMINA_IMPROVEMENT', '체력 증진'
        CALORIE_BURN = 'CALORIE_BURN', '칼로리 소모'
        FLEXIBILITY_IMPROVEMENT = 'FLEXIBILITY_IMPROVEMENT', '유연성 향상'

    milestone_id = models.AutoField(primary_key=True, verbose_name="중간 목표 ID")
    sport_milestone = models.CharField(max_length=100, choices=SportMilestoneChoices.choices, verbose_name="중간 목표")
    sport_type = models.ForeignKey(SportType, on_delete=models.CASCADE, related_name='sport_milestones', verbose_name="운동 종목")

    def __str__(self):
        return f"{self.sport_milestone}"

    class Meta:
        verbose_name = "운동 중간 목표"
        verbose_name_plural = "운동 중간 목표들"


class SportSession(BaseModel):
    '''운동세션'''

    session_id = models.AutoField(primary_key=True, verbose_name="세션 ID")
    exercise_video = models.FileField(null=True, blank=True, upload_to='video/', verbose_name="운동 영상")
    exercise_at = models.DateTimeField(verbose_name="운동 시간")
    exercise_loc = models.CharField(max_length=100, verbose_name="운동 장소")
    exercise_dur = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="운동 시간(분)")

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sport_sessions', verbose_name="사용자")


    def __str__(self):
        return f"{self.exercise_at} at {self.exercise_loc} by {self.user.username}"

    class Meta:
        verbose_name = "운동 세션"
        verbose_name_plural = "운동 세션들"

class Category(BaseModel):
    '''카테고리'''
    name = models.CharField(max_length=100, verbose_name="카테고리명")
    slug = models.SlugField(unique=True, verbose_name="슬러그")
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "카테고리"
        verbose_name_plural = "카테고리들"

class Tag(BaseModel):
    '''태그'''
    name = models.CharField(max_length=100, unique=True, verbose_name="태그명")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="슬러그")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "태그"
        verbose_name_plural = "태그들"


class Post(BaseModel):
    '''게시글'''
    post_id = models.AutoField(primary_key=True, verbose_name="게시글 ID")
    post_title = models.CharField(max_length=100, verbose_name="제목")
    post_content = models.TextField(verbose_name="내용")
    
    post_user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name='posts', blank=True, null=True, verbose_name="작성자") # 익명의 게시물 허용
    post_sport_type = models.ForeignKey(SportType, on_delete=models.PROTECT, related_name='posts', verbose_name="운동 종목")
    post_sport_milestone = models.ForeignKey(SportMilestone, on_delete=models.PROTECT, related_name='posts', verbose_name="운동 목표")
    post_session = models.OneToOneField(SportSession, on_delete=models.CASCADE, verbose_name="운동 세션")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts', verbose_name="카테고리")
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True, verbose_name="태그")

    @property
    def milestone_progress_count(self):
        return MilestoneProgress.objects.get(pg_sport_type=self.sport_type, pg_sport_milestone=self.sport_milestone).post_count

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        MilestoneProgress.increment_count(self.sport_type, self.sport_milestone)
        
        
    def __str__(self): 
        return f"{self.title} by {self.user.username if self.user else 'Anonymous'}"

class Comment(BaseModel):
    '''댓글'''
    comment_id = models.AutoField(primary_key=True, verbose_name="댓글 ID")
    comment_content = models.TextField(verbose_name="내용")
    comment_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_comments', verbose_name="작성자")
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments', verbose_name="게시글")
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies', verbose_name="부모 댓글")

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"

    class Meta:
        verbose_name = "댓글"
        verbose_name_plural = "댓글들"


class MilestoneProgress(BaseModel):
    '''목표진행'''
    m_progress_id = models.AutoField(primary_key=True, verbose_name="진행 ID")
    post_count = models.PositiveSmallIntegerField(default=0, verbose_name="게시글 수")
    pg_sport_type = models.ForeignKey(SportType, on_delete=models.CASCADE, related_name='sport_progress', verbose_name="운동 종목")
    pg_sport_milestone = models.ForeignKey(SportMilestone, on_delete=models.CASCADE, related_name='milestone_progress', verbose_name="운동 목표")

    class Meta:
        unique_together = ('pg_sport_type', 'pg_sport_milestone')

        verbose_name = "목표 진행"
        verbose_name_plural = "목표 진행들"

    def __str__(self):
        return f"{self.pg_sport_type} - {self.pg_sport_milestone}: {self.post_count}"
    
    @classmethod
    def increment_count(cls, sport_type, sport_milestone):
        """
        주어진 sport_type과 sport_milestone에 해당하는 MilestoneProgress의
        post_count를 증가시키고 증가된 값을 반환하는 메서드
        """
        milestone_progress, _ = cls.objects.get_or_create(
            pg_sport_type=sport_type,
            pg_sport_milestone=sport_milestone
        )
        milestone_progress.post_count = models.F('post_count') + 1
        milestone_progress.save()           
