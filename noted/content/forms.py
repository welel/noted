from django import forms
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _

from content.models import Source, Note


class NoteForm(forms.ModelForm):
    source_type = forms.ChoiceField(
        choices=Source.TYPES,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Note
        fields = (
            "title",
            "source_type",
            "source",
            "body_raw",
            "summary",
            "anonymous",
        )
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control form-control-lg",
                    "placeholder": _("Title"),
                }
            ),
            "source": forms.TextInput(
                attrs={
                    "list": "source-list",
                    "autocomplete": "off",
                }
            ),
            "summary": forms.TextInput(
                attrs={"class": "form-control", "placeholder": _("Summary")}
            ),
            "anonymous": forms.CheckboxInput(
                attrs={"class": "form-check-input", "role": "switch"}
            ),
        }


# class SourceForm(forms.ModelForm):
#     class Meta:
#         model = Source
#         fields = ("sourcename", "type")


# CLEATE ONE FORM AND HANDLE ALL FIELDS HARDCODLY
# ModelChoiceField

# class NoteForm(forms.Form):
#     title = forms.CharField(
#         max_length=100, min_length=3, required=True
#     )
#     source_type = forms.CharField()
#     source_title = forms.CharField(
#         max_length=200, min_length=3
#     )
#     body_raw = ""
#     summary = forms.CharField(
#         max_length=250, min_length=5
#     )
#     anonymous = forms.BooleanField()
