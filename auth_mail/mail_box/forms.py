from django import forms

class ComposeForm(forms.Form):
    to = forms.EmailField()
    subject = forms.CharField(max_length=100)
    body = forms.CharField(widget=forms.Textarea)
    document = forms.Field(widget=forms.FileInput)