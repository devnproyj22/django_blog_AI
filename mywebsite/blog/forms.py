import re
from django import forms
from .models import Post, Comment, SportSession
from django.utils.translation import gettext_lazy as _
from django.conf import settings

def check_inappropriate_words(text, word_list):
    for word in word_list:
        if re.search(r'\b' + re.escape(word) + r'\b', text.lower()):
            return word
    return None

class PostForm(forms.ModelForm):
    exercise_video = forms.FileField(required=False)  
    exercise_at = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    exercise_loc = forms.CharField(max_length=100)
    exercise_dur = forms.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        model = Post
        fields = ['post_title', 'post_content', 'post_sport_type', 'post_sport_milestone', 
                  'exercise_video', 'exercise_at', 'exercise_loc', 'exercise_dur']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  
        self.fields['post_sport_type'].widget = forms.Select()
        self.fields['post_sport_milestone'].widget = forms.Select()

        if self.instance and self.instance.pk:
            if self.instance.post_session:
                self.fields['exercise_at'].initial = self.instance.post_session.exercise_at
                self.fields['exercise_loc'].initial = self.instance.post_session.exercise_loc
                self.fields['exercise_dur'].initial = self.instance.post_session.exercise_dur
                self.fields['exercise_video'].initial = self.instance.post_session.exercise_video

    def clean_post_title(self):
        post_title = self.cleaned_data.get('post_title')
        inappropriate_word = check_inappropriate_words(post_title, settings.POST_INAPPROPRIATE_WORDS)
        if inappropriate_word:
            raise forms.ValidationError(_('게시글 제목에 부적절한 단어 "%(word)s"가 포함되어 있습니다'), 
                                        params={'word': inappropriate_word})
        return post_title

    def clean_post_content(self):
        post_content = self.cleaned_data.get('post_content')
        inappropriate_word = check_inappropriate_words(post_content, settings.POST_INAPPROPRIATE_WORDS)
        if inappropriate_word:
            raise forms.ValidationError(_('게시글 내용에 부적절한 단어 "%(word)s"가 포함되어 있습니다'), 
                                        params={'word': inappropriate_word})
        return post_content

    def clean_exercise_video(self):
        exercise_video = self.cleaned_data.get('exercise_video')
        if exercise_video:
            if exercise_video.size > settings.MAX_UPLOAD_SIZE:
                raise forms.ValidationError(_('업로드된 파일이 너무 큽니다. 최대 %(size)sMB까지 허용됩니다.'),
                                            params={'size': settings.MAX_UPLOAD_SIZE // (1024 * 1024)})
            file_type = exercise_video.content_type.split('/')[1]
            if file_type not in settings.ALLOWED_VIDEO_TYPES:
                raise forms.ValidationError(_('지원되지 않는 파일 형식입니다. 허용된 형식: %(types)s'),
                                            params={'types': ', '.join(settings.ALLOWED_VIDEO_TYPES)})
        return exercise_video

    def clean_exercise_loc(self):
        exercise_loc = self.cleaned_data.get('exercise_loc')
        inappropriate_word = check_inappropriate_words(exercise_loc, settings.INAPPROPRIATE_WORDS['place'])
        if inappropriate_word:
            raise forms.ValidationError(_('운동 장소에 부적절한 단어 "%(word)s"가 포함되어 있습니다'), 
                                        params={'word': inappropriate_word})
        return exercise_loc
        
    def clean_exercise_dur(self):
        exercise_dur = self.cleaned_data.get('exercise_dur')
        if exercise_dur and exercise_dur <= 0:
            raise forms.ValidationError(_('운동 시간은 양수여야 합니다'))
        return exercise_dur

    def clean_exercise_at(self):
        exercise_at = self.cleaned_data.get('exercise_at')
        if not exercise_at:
            raise forms.ValidationError(_('운동 날짜와 시간은 필수입니다'))
        return exercise_at
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.post_session:
            instance.post_session = SportSession() 

        instance.post_session.exercise_at = self.cleaned_data.get('exercise_at')
        instance.post_session.exercise_loc = self.cleaned_data.get('exercise_loc')
        instance.post_session.exercise_dur = self.cleaned_data.get('exercise_dur')
        instance.post_session.exercise_video = self.cleaned_data.get('exercise_video')

        if commit:
            instance.post_session.save() 
            instance.save()  

        return instance


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_content']  

    def clean_comment_content(self):
        comment_content = self.cleaned_data.get('comment_content')
        inappropriate_word = check_inappropriate_words(comment_content, settings.INAPPROPRIATE_WORDS['comment'])
        if inappropriate_word:
            raise forms.ValidationError(_('댓글에 부적절한 단어 "%(word)s"가 포함되어 있습니다'), 
                                        params={'word': inappropriate_word})
        return comment_content
