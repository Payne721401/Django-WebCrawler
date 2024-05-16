from typing import Any
from django import forms
from django.core import validators
from django.contrib.auth.models import User
from fapp.models import UserProfile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username','email', 'password',)
    # name = forms.CharField(validators= [check_for_z])
    # email = forms.EmailField(max_length=100, label='Email')
    # verifyemail = forms.EmailField(max_length=100, label='Verify your email address')
    # text = forms.CharField(widget=forms.Textarea)
    # botcatcher = forms.CharField(required=False,
    #                              widget=forms.HiddenInput,
    #                              validators=[validators.MaxLengthValidator(0)])
    
    #validate the form, equivalent to validators

    # def clean_botcatcher(self) -> dict[str, Any]:
    #     botcatcher = self.cleaned_data['botcatcher']
    #     if len(botcatcher) > 0:
    #         raise forms.ValidationError("Gotcha Bot")
        
    #     return botcatcher
                                
    #Clean All data and dael with them

    #  def clean(self):
    #     all_clean_data = super().clean()
    #     email  = all_clean_data['email']
    #     vemail = all_clean_data['verifyemail']

    #     if email!= vemail:
    #         raise forms.ValidationError('Email and verify email do not match')

# class UserProfileForm(forms.ModelForm):
#     class Meta():
#         model = UserProfile
#         fields = ('portfolio_site', 'profile_pic')
        # fields = ('portfolio_site')


   
