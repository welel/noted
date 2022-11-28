from django import forms

from content.models import Source, Note
from django.utils.translation import gettext_lazy as _


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
                    "placeholder": _("Title"),
                }
            ),
            "summary": forms.TextInput(
                attrs={"class": "form-control", "placeholder": _("Summary")}
            ),
            "anonymous": forms.CheckboxInput(
                attrs={"class": "form-check-input", "role": "switch"}
            ),
        }
