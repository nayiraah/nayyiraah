from django import forms

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    # Honeypot field: real visitors never fill this in (it's hidden with CSS).
    # Simple bot-deterrent that needs no external service or JS challenge.
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "message"]
        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "Your name", "autocomplete": "name", "maxlength": 120,
            }),
            "email": forms.EmailInput(attrs={
                "placeholder": "you@example.com", "autocomplete": "email",
            }),
            "message": forms.Textarea(attrs={
                "placeholder": "What would you like to tell us?", "rows": 6,
            }),
        }

    def clean_website(self):
        value = self.cleaned_data.get("website")
        if value:
            raise forms.ValidationError("Spam detected.")
        return value

    def clean_message(self):
        message = self.cleaned_data["message"].strip()
        if len(message) < 5:
            raise forms.ValidationError("Please write a little more so we know how to help.")
        return message
