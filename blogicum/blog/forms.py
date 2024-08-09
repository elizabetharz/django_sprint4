from django import forms
from blog.models import Post, Comment
from django.utils import timezone


class PostForm(forms.ModelForm):
    """Форма поста на основе модели."""

    def __init__(self, *args, **kwargs):
        """Заполнение поля pub_date."""
        super().__init__(*args, **kwargs)
        self.fields['pub_date'].initial = timezone.localtime(
            timezone.now()
        ).strftime('%Y-%m-%dT%H:%M')

    class Meta:
        """Метакласс."""

        model = Post
        exclude = ('author',)
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }


class CommentForm(forms.ModelForm):
    """Форма комментариев на основе модели."""

    class Meta:
        """Метакласс."""

        model = Comment
        fields = ('text',)
