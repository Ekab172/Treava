from django import forms

from .models import CoachingRequest


class ToolSignupForm(forms.Form):
    email = forms.EmailField(
        max_length=254,
        label="Email address",
        widget=forms.EmailInput(
            attrs={"id": "lemail", "autocomplete": "email", "placeholder": "you@example.com"}
        ),
    )

    def clean_email(self):
        return self.cleaned_data["email"].lower()


class CoachingRequestForm(forms.ModelForm):
    topic = forms.ChoiceField(
        choices=CoachingRequest.Topic.choices,
        initial=CoachingRequest.Topic.PRICING,
        label="What do you need help with?",
        widget=forms.Select(attrs={"id": "ct"}),
    )

    class Meta:
        model = CoachingRequest
        fields = ["name", "email", "topic", "message"]
        labels = {
            "name": "Your name",
            "email": "Email address",
            "topic": "What do you need help with?",
            "message": "Message",
        }
        widgets = {
            "name": forms.TextInput(attrs={"id": "cn", "autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"id": "ce", "autocomplete": "email"}),
            "topic": forms.Select(attrs={"id": "ct"}),
            "message": forms.Textarea(attrs={"id": "cm", "rows": 4}),
        }

    def clean_email(self):
        return self.cleaned_data["email"].lower()
