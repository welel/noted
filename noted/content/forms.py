from django import forms

from content.models import Source, Note


class SourceForm:
    pass


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ("title", "body_raw", "summary", "anonymous")
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control form-control-lg",
                    "placeholder": "Title",
                }
            ),
            "summary": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Summary"}
            ),
            "anonymous": forms.CheckboxInput(
                attrs={"class": "form-check-input", "role": "switch"}
            ),
        }
