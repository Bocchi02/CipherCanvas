from django import forms

class EncodeForm(forms.Form):
    image = forms.ImageField()
    secret_message = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 6,
            'placeholder': 'Enter your secret message here...'
        })
    )