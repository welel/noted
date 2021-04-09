from django.core.exceptions import ValidationError
from django.forms import ModelForm, TextInput, CheckboxInput

from taggit.forms import TagWidget

from notes.models import Note


class NoteForm(ModelForm):

    class Meta:
        model = Note
        fields = [
            'title', 'source', 'private', 'anonymous',
            'tags', 'body_raw', 'summary'
        ]
        widgets = {
            'tags': TagWidget(attrs={'data-role': 'tagsinput'}),
        }

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        if len(tags) > 5:
            raise ValidationError('You can add only 5 tags.')
        for i, tag in enumerate(tags):
            if len(tag) > 25:
                raise ValidationError(
                    'Length of a tag should be less than 25 symbols.'
                )
        return tags
