from django import forms
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm



class FormSettings(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormSettings, self).__init__(*args, **kwargs)
        # Here make some changes such as:
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'w-full py-2 px-3 border border-gray-300 rounded-lg focus:outline-none focus:border-green-400'

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'border w-full px-2 py-2 focus:outline-none focus:ring-0 text-base focus:border-gray-600','placeholder':'Enter Username'})
        self.fields['first_name'].widget.attrs.update({'class': 'border w-full px-2 py-2 focus:outline-none focus:ring-0 text-base focus:border-gray-600', 'placeholder':'Enter Your First Name'})
        self.fields['last_name'].widget.attrs.update({'class': 'border w-full px-2 py-2 focus:outline-none focus:ring-0 text-base focus:border-gray-600','placeholder':'Enter Your Last Name'})
        self.fields['email'].widget.attrs.update({'class': 'border w-full px-2 py-2 focus:outline-none focus:ring-0 text-base focus:border-gray-600','placeholder':'Enter email@exm.com'})
        self.fields['password1'].widget.attrs.update({'class': 'border w-full px-2 py-2 focus:outline-none focus:ring-0 text-base focus:border-gray-600','placeholder':'Enter Password'})
        self.fields['password2'].widget.attrs.update({'class': 'border w-full px-2 py-2 focus:outline-none focus:ring-0 text-base focus:border-gray-600','placeholder':'Enter confirm Password'})
        
        
class Changepass(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'border w-full px-2 py-2 focus:outline-none focus:ring-0 text-base focus:border-gray-600','placeholder':'Enter Old Password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'border w-full px-2 py-2 focus:outline-none focus:ring-0 text-base focus:border-gray-600','placeholder':'Enter New Password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'border w-full px-2 py-2 focus:outline-none focus:ring-0 text-base focus:border-gray-600','placeholder':'Enter confirm New Password'}))
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']
    


class Change_pass(SetPasswordForm):   
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']
        
    def __init__(self, *args, **kwargs):
        super(Change_pass, self).__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({'class': 'border w-full px-2 py-2 focus:outline-none focus:ring-0 text-base focus:border-gray-600','placeholder':'Enter New Password'})
        self.fields['new_password2'].widget.attrs.update({'class': 'border w-full px-2 py-2 focus:outline-none focus:ring-0 text-base focus:border-gray-600','placeholder':'Enter Confirm New Password'})
    