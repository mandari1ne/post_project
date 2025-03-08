from django import forms
from django.contrib.auth import get_user_model


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
