from django import forms
from .models import Post, Comment
from users.models import CustomUser


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body',)


class SearchForm(forms.Form):
    query = forms.CharField()


class FliterForm(forms.Form):
    year = forms.IntegerField(label='Enter year', required=False)
    author = forms.CharField(label='Enter author post', required=False)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)