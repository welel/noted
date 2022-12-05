from django import forms
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
                attrs={"autocomplete": "off", "class": "form-control"}
            ),
            "summary": forms.TextInput(
                attrs={"class": "form-control", "placeholder": _("Summary")}
            ),
            "anonymous": forms.CheckboxInput(
                attrs={"class": "form-check-input", "role": "switch"}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        if self.data["source"]:
            source, _ = Source.objects.get_or_create(
                type=cleaned_data["source_type"], title=self.data["source"]
            )
            cleaned_data["source"] = source
            del self.errors["source"]
