from django import forms
from .models import Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comment



class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "form-control",
                "placeholder": field.label,
            })
    

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "category",
            "tags",
            "image",
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            field.widget.attrs["class"] = "form-control"



class CommentForm(forms.ModelForm):

    class Meta:

        model = Comment

        fields = [

            "text"

        ]