from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from common.models import BaseModel  

class CustomUser(AbstractUser, BaseModel):
    nickname = models.CharField(max_length=30, unique=True, verbose_name=_('닉네임'))
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True, verbose_name=_('프로필 사진'))
    
    AGE_RANGE_CHOICES = [
        ('10-19', '10대'),
        ('20-29', '20대'),
        ('30-39', '30대'),
        ('40-49', '40대'),
        ('50+', '50대+'),
    ]
    
    age_range = models.CharField(max_length=5, choices=AGE_RANGE_CHOICES, blank=True, verbose_name=_('연령대'))
    area_of_interest = models.TextField(blank=True, verbose_name=_('관심 분야'))
    
    def __str__(self):
        return self.username

