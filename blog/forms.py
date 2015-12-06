from django import forms
from blog.models import Blog

class CreateBlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        exclude = ['posted', 'author']
