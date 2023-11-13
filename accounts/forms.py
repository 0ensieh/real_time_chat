# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - sharifdata sdata.ir
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, VerificationCode
from django.db.models import Q

# ------------------------------ User SignUp ------------------------------
    
class SignUpForm(UserCreationForm):
    GENDER_CHOICES = [
        ('1', 'مرد'),
        ('2', 'زن  '),
    ]

    password1 = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={'dir': 'ltr', 'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='تکرار رمز عبور',
        widget=forms.PasswordInput(attrs={'dir': 'ltr', 'class': 'form-control'})
    )
    # gender = forms.ChoiceField(
    #     label='جنسیت',
    #     choices=GENDER_CHOICES,
    #     widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    # )
    gender = forms.ChoiceField(label='جنسیت', choices=GENDER_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'email', 'gender')
        widgets = {
            'first_name': forms.TextInput(attrs={'dir': 'rtl', 'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'dir': 'rtl', 'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'dir': 'ltr'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'dir': 'ltr'}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = 'رمز عبور'
        self.fields['password2'].label = 'تکرار رمز عبور'




# ------------------------------ User Login ------------------------------
class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "شماره موبایل / ایمیل / نام کاربری",
                "class": "form-control",
                "dir": "rtl",
                "title": "", 
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "کلمه عبور",
                "class": "form-control",
                "dir": "rtl",
                "title": ""
            }
        ))



class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ProfileForm, self).__init__(*args, **kwargs)


    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control mt-5', 'placeholder': 'نام چت را وارد کنید...'}), 
            'email': forms.EmailInput(attrs={'class': 'form-control mt-5', 'placeholder': 'نام چت را وارد کنید...'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control mt-5', 'placeholder': 'نام چت را وارد کنید...'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control mt-5', 'placeholder': 'نام چت را وارد کنید...'})

            
        }
     

