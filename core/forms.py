from django import forms
from .models import ContactMessage,SunshineEntry,WorkEntry


class ContactForm(forms.ModelForm):
    website=forms.CharField(
        required=False,
        widget=forms.HiddenInput
    )

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "phone", "message"]

        widgets={
            "name": forms.TextInput(attrs={
                "placeholder": "Your name",
                "autocomplete": "name",
                "maxlength": 120,
            }),
            "email": forms.EmailInput(attrs={
                "placeholder": "you@example.com",
                "autocomplete": "email",
            }),
            "message": forms.Textarea(attrs={
                "placeholder": "What would you like to tell us?",
                "rows": 6,
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
            raise forms.ValidationError(
                "Please write a little more so we know how to help."
            )
        return message

class SunshineEntryForm(forms.ModelForm):
    class Meta:
        model=SunshineEntry
        fields=["date","quote","meaning","reminder","affirmation","is_published",]

        widgets={
             "date": forms.DateInput(
                attrs={"type": "date"}
             ),
             "quote": forms.TextInput(
                attrs={
                    "placeholder": "Today's quote"
                }
            ),
            "meaning": forms.Textarea(
                attrs={
                    "placeholder": "What does this quote mean?",
                    "rows": 4
                }
            ),
            "reminder": forms.TextInput(
                attrs={
                    "placeholder": "Today's reminder"
                }
            ),
            "affirmation": forms.TextInput(
                attrs={
                    "placeholder": "Today's affirmation"
                }
            ),
        }

class WorkEntryForm(forms.ModelForm):
    class Meta:
        model = WorkEntry
        fields = [
            "title",
            "date",
            "location",
            "summary",
            "body",
            "cover_image",
            "is_published",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "Title of the activity"
                }
            ),
            "date": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),
            "location": forms.TextInput(
                attrs={
                    "placeholder": "Where did this activity happen?"
                }
            ),
            "summary": forms.TextInput(
                attrs={
                    "placeholder": "Short description of the activity"
                }
            ),
            "body": forms.Textarea(
                attrs={
                    "placeholder": "Write about the activity...",
                    "rows": 8
                }
            ),
            "cover_image": forms.ClearableFileInput(),
        }


