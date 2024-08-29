from django.db import models


# Base model with created_at and updated_at fields
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, unique=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# SportType model (운동종목)
class SportType(BaseModel):
    class SportTypeChoices(models.TextChoices):
        GOLF = 'GOLF', '골프'
        TENNIS = 'TENNIS', '테니스'
        PILATES = 'PILATES', '필라테스'
        JOGGING = 'JOGGING', '조깅'
        HIKING = 'HIKING', '등산'
        SWIMMING = 'SWIMMING', '수영'

    sport_id = models.AutoField(primary_key=True)
    sport_type = models.CharField(max_length=100, choices=SportTypeChoices.choices, unique=True)

    def __str__(self):
        return f"{self.sport_type}"

# SportMilestone model (운동목표)
class SportMilestone(BaseModel):
    class SportMilestoneChoices(models.TextChoices):
        RECORD_IMPROVEMENT = 'RECORD_IMPROVEMENT', '기록단축'
        REPETITIONS_INCREASE = 'REPETITIONS_INCREASE', '반복 횟수 증가'
        DISTANCE_EXTENSION = 'DISTANCE_EXTENSION', '거리연장'
        SKILL_IMPROVEMENT = 'SKILL_IMPROVEMENT', '기술 향상'
        CONSISTENCY = 'CONSISTENCY', '일정 유지'
        STAMINA_IMPROVEMENT = 'STAMINA_IMPROVEMENT', '체력 증진'
        CALORIE_BURN = 'CALORIE_BURN', '칼로리 소모'
        FLEXIBILITY_IMPROVEMENT = 'FLEXIBILITY_IMPROVEMENT', '유연성 향상'

    milestone_id = models.AutoField(primary_key=True)
    sport_milestone = models.CharField(max_length=100, choices=SportMilestoneChoices.choices)
    sport_type = models.ForeignKey(SportType, on_delete=models.CASCADE, related_name='sport_milestones')

    def __str__(self):
        return f"{self.sport_milestone} for {self.sport_type}"

# SportSession model (운동세션)
class SportSession(BaseModel):
    session_id = models.AutoField(primary_key=True)
    exercise_video = models.FileField(null=True, blank=True, upload_to='video/')
    exercise_at = models.DateTimeField()
    exercise_loc = models.CharField(max_length=100)
    exercise_dur = models.DecimalField(max_digits=5, decimal_places=2)
    session_user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='user_sessions')

    def __str__(self):
        return f"{self.exercise_at} at {self.exercise_loc} by {self.session_user.username}"

# Post model (게시글)
class Post(BaseModel):
    post_id = models.AutoField(primary_key=True)
    post_title = models.CharField(max_length=100)
    post_content = models.TextField()
    milestone_progress_count = models.PositiveSmallIntegerField()
    post_user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='user_posts')
    post_sport_type = models.ForeignKey(SportType, on_delete=models.CASCADE, related_name='sport_posts')
    post_sport_milestone = models.ForeignKey(SportMilestone, on_delete=models.CASCADE, related_name='milestone_posts')
    post_session = models.OneToOneField(SportSession, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.pk:  # 새 게시글인 경우
            self.milestone_progress_count = MilestoneProgress.increment_and_get_count(
                self.post_sport_type, self.post_sport_milestone
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.post_title} by {self.post_user.username}"

# Comment model (댓글)
class Comment(BaseModel):
    comment_id = models.AutoField(primary_key=True)
    post_comment = models.TextField()
    comment_user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='user_comments')
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    c_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='c_comments')

    def __str__(self):
        return f"Comment by {self.comment_user.username} on {self.comment_post.post_title}"

# MilestoneProgress model (목표진행)
class MilestoneProgress(BaseModel):
    m_progress_id = models.AutoField(primary_key=True)
    post_count = models.PositiveSmallIntegerField(default=0)
    pg_sport_type = models.ForeignKey(SportType, on_delete=models.CASCADE, related_name='sport_progress')
    pg_sport_milestone = models.ForeignKey(SportMilestone, on_delete=models.CASCADE, related_name='milestone_progress')

    class Meta:
        unique_together = ('pg_sport_type', 'pg_sport_milestone')

    def __str__(self):
        return f"{self.pg_sport_type} - {self.pg_sport_milestone}: {self.post_count}"
