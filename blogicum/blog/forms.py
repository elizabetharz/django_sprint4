from django import forms
from blog.models import Post, Comment


class PostForm(forms.ModelForm):
    """Форма поста на основе модели."""

    class Meta:
        """Метакласс."""

        model = Post
        fields = '__all__'


class CommentForm(forms.ModelForm):
    """Форма комментариев на основе модели."""

    class Meta:
        """Метакласс."""

        model = Comment
        fields = ('text',)
