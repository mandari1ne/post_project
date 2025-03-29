from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


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

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают.")

        try:
            validate_password(password2)
        except ValidationError as e:
            for error in e.messages:
                if error == "This password is too short. It must contain at least 8 characters.":
                    raise forms.ValidationError("Пароль слишком короткий. Он должен содержать хотя бы 8 символов.")
                if error == "This password is too common.":
                    raise forms.ValidationError("Пароль слишком простой.")
                if error == "This password is entirely numeric.":
                    raise forms.ValidationError("Пароль состоит только из цифр.")
                else:
                    raise forms.ValidationError(error)

        return password2
