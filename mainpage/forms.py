from django import forms
from django.contrib.auth.models import User
from .models import ContactUs


class UserRegisterForm(forms.Form):
    user_name = forms.CharField(label='', max_length=30, widget=forms.TextInput(attrs={'placeholder': ' نام کاربری'}))
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'placeholder': 'ایمیل'}))
    first_name = forms.CharField(label='', max_length=30, widget=forms.TextInput(attrs={'placeholder': 'نام'}))
    last_name = forms.CharField(label='', max_length=30, widget=forms.TextInput(attrs={'placeholder': 'نام خانوادگی'}))
    password1 = forms.CharField(label='', max_length=50, widget=forms.PasswordInput(attrs={'placeholder': 'رمز'}))
    password2 = forms.CharField(label='', max_length=50, widget=forms.PasswordInput(attrs={'placeholder': 'تکرار رمز'}))

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['user_name'].initial = 'نام کاربری'

    # _____________________validation__________________________
    def clean_user_name(self):
        user = self.cleaned_data['user_name']
        if User.objects.filter(username=user).exists():
            raise forms.ValidationError('این کاربر وجود دارد')
        return user

    # _____________________email__________________________
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('این ایمیل وجود دارد')
        return email

    # _____________________password__________________________
    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError('رمز را درست وارد کنید')
        elif len(password2) <= 8:
            raise forms.ValidationError('رمز کوتاه است')
        elif not any(i.isupper() for i in password2):
            raise forms.ValidationError('لطفا از A-a استفاده کنید')
        return password2


class UserLogInForm(forms.Form):
    user = forms.CharField(label='نام کاربر', max_length=30,
                           widget=forms.TextInput(attrs={'placeholder': ' نام کاربری'}))
    password = forms.CharField(label='رمزعبور', max_length=50, widget=forms.PasswordInput(attrs={'placeholder': 'رمز'}))


class LogoutForm(forms.Form):
    username = forms.CharField(label='نام کاربر', max_length=30,
                               widget=forms.TextInput(attrs={'placeholder': ' نام کاربری'}))
    password = forms.CharField(label='رمزعبور', max_length=50, widget=forms.PasswordInput(attrs={'placeholder': 'رمز'}))


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['name', 'email', 'title', 'message']
