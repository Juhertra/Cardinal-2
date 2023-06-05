from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

class CustomUserCreationForm(UserCreationForm):
    roles = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Roles"
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2', 'roles')
