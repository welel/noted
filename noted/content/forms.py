from taggit.forms import TagWidget

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Note, Source


class NoteForm(forms.ModelForm):
    """A form for creating/updating :model:`Note` and :model:`Source`.

    A note can have a source. The form handles creating a note and a source.

    """

    source_type = forms.ChoiceField(
        choices=Source.TYPES,
        widget=forms.Select(attrs={"class": "form-select"}),
        label=_("Source Type"),
    )
    source_link = forms.URLField(
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control d-inline form-control-sm ms-2",
                "placeholder": _("Link"),
            }
        ),
        label=_("Source link"),
    )
    source_description = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control d-inline form-control-sm ms-2",
                "placeholder": _("Description in 100 characters."),
            }
        ),
        label=_("Source Description"),
    )

    class Meta:
        model = Note
        fields = (
            "title",
            "source_type",
            "source",
            "body_raw",
            "tags",
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
            "tags": TagWidget(attrs={"data-role": "tagsinput"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.source:
            self.initial.update(
                {
                    "source": self.instance.source.title,
                    "source_type": self.instance.source.type,
                    "source_link": self.instance.source.link,
                    "source_description": self.instance.source.description,
                }
            )

    def clean_body_raw(self):
        body_raw = self.cleaned_data.get("body_raw")
        if not body_raw:
            raise ValidationError(_("Note text can't be empty."))
        return body_raw

    def clean_tags(self):
        """Validates the `tags` field.

        Validates the number of tags (less than 4) and tag length
        (less than 25 symbols).
        """
        tags = self.cleaned_data["tags"]
        if len(tags) > 3:
            raise ValidationError(_("You can add only 3 tags."))
        for i, tag in enumerate(tags):
            if len(tag) > 25:
                raise ValidationError(
                    _(
                        f"Length of {i+1} tag should be \
                            less than 25 symbols."
                    )
                )
        return tags

    def clean(self):
        cleaned_data = super().clean()
        if self.data.get("source"):
            source, _ = Source.objects.get_or_create(
                type=cleaned_data["source_type"],
                title=self.data["source"],
                link=cleaned_data.get("source_link", ""),
                description=cleaned_data["source_description"],
            )
            cleaned_data["source"] = source
            if "source" in self.errors:
                del self.errors["source"]
