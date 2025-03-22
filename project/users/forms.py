from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()

        fields = ['username', 'first_name', 'last_name', 'email', 'icon']

        widgets = {
            'icon': forms.ClearableFileInput(attrs={'multiple': True}),
        }

    def clean_username(self):
        username = self.cleaned_data['username']

        if get_user_model().objects.filter(username=username).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("Такой пользователь существует")

        return username

    def clean_email(self):
        email = self.cleaned_data['email']

        if get_user_model().objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("Такой email уже зарегистрирован")

        return email


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    icon = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2', 'icon']

    def clean_username(self):
        username = self.cleaned_data['username']

        if get_user_model().objects.filter(username=username).exists():
            raise forms.ValidationError("Пользователь с таким именем уже существует.")

        return username

    def clean_email(self):
        email = self.cleaned_data['email']

        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует.")

        return email
