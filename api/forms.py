from django import forms
from django.forms import Textarea
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({'class': 'text-black border  rounded-md w-full px-2 py-2 focus:outline-none focus:ring-0 text-base focus:border-gray-600', 'placeholder':'Enter Your Full Name'})
        self.fields['email'].widget.attrs.update({'class': 'text-black border rounded-md w-full px-2 py-2 focus:outline-none focus:ring-0 text-base focus:border-gray-600', 'placeholder':'Enter Your Active Email'})
        self.fields['phone'].widget.attrs.update({'class': 'text-black border rounded-md w-full px-2 py-2 focus:outline-none focus:ring-0 text-base focus:border-gray-600', 'placeholder':'Enter Your Phone Number'})
        self.fields['message'].widget.attrs.update({'class': 'text-black border rounded-md w-full px-2 py-2 focus:outline-none focus:ring-0 text-base focus:border-gray-600', 'placeholder':'Write Your Message'})

    class Meta:
        model = ContactMessage
        fields = ['name', 'email','phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'border w-50 px-2 py-2 focus:outline-none focus:ring-0 text-base focus:border-gray-600'}),
            'email': forms.TextInput(attrs={'class': 'border w-50 px-2 py-2 focus:outline-none focus:ring-0 text-base focus:border-gray-600'}),
            'phone': forms.TextInput(attrs={'class': 'border w-50 px-2 py-2 focus:outline-none focus:ring-0 text-base focus:border-gray-600'}),
            'message': Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        } 