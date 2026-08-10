import re
from django import forms
from .models import Candidate


class VoteForm(forms.Form):
    voter_id = forms.CharField(
        required=False,
        max_length=20,
        label="Voter ID",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Demo Voter ID",
            "autocomplete": "off",
        }),
    )
    aadhaar_id = forms.CharField(
        required=False,
        max_length=12,
        label="Aadhaar / Demo ID",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Use a dummy 12-digit value only",
            "inputmode": "numeric",
            "autocomplete": "off",
        }),
    )
    candidate = forms.ModelChoiceField(
        queryset=Candidate.objects.none(),
        empty_label=None,
        widget=forms.RadioSelect,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["candidate"].queryset = Candidate.objects.filter(active=True)

    def clean(self):
        cleaned = super().clean()
        voter_id = (cleaned.get("voter_id") or "").strip().upper()
        aadhaar_id = (cleaned.get("aadhaar_id") or "").strip()

        if not voter_id and not aadhaar_id:
            raise forms.ValidationError("Enter a demo Voter ID or demo 12-digit ID.")

        if voter_id and not re.fullmatch(r"[A-Z0-9-]{3,20}", voter_id):
            raise forms.ValidationError("Voter ID may contain letters, numbers, and hyphens only.")

        if aadhaar_id and not re.fullmatch(r"\d{12}", aadhaar_id):
            raise forms.ValidationError("The demo Aadhaar-style ID must contain exactly 12 digits.")

        # Do not store either identifier in plaintext.
        cleaned["verification_value"] = voter_id or aadhaar_id
        return cleaned
