from django import forms
from .models import User, Post
from django.contrib.auth.forms import AuthenticationForm
from Quora.models import Answer


class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password'
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()
        return user


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'user',
            'question'
        ]

    def save(self, commit=True):
        post = super().save(commit=False)
        post.question = self.cleaned_data['question']

        if commit:
            post.save()
        return post


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = [
            'user',
            'original_post',
            'content'
        ]

    def save(self, commit=True):
        answer = super().save(commit=False)
        answer.content = self.cleaned_data['content']

        if commit:
            answer.save()

        return answer
