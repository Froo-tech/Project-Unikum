from django import forms

class LoginUserForm(forms.Form):
    username = forms.CharField(label="Логин",
                               widget=forms.TextInput(attrs={'calss': 'from-input'}))
    password = forms.CharField(label="Пароль",
                               widget=forms.PasswordInput(attrs={'calss': 'from-input'}))