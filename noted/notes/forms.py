from django.core.exceptions import ValidationError
from django import forms

from taggit.forms import TagWidget
from mptt.forms import TreeNodeChoiceField

from notes.models import Note, Comment


class NoteForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body_raw'].label = ''

    class Meta:
        model = Note
        fields = [
            'title', 'source', 'private', 'anonymous', 'allow_comments',
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
                    f'Length of {i+1} tag should be less than 25 symbols.'
                )
        return tags


class CommentForm(forms.ModelForm):
    parent = TreeNodeChoiceField(queryset=Comment.objects.root_nodes())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].widget.attrs.update({'class': 'd-none'})
        self.fields['parent'].label = ''
        self.fields['parent'].required = False
        self.fields['content'].label = ''

    class Meta:
        model = Comment
        fields = ('parent', 'content',)
        widgets = {
            'content': forms.Textarea(
                attrs={'class': 'form-control shadow-none',
                       'placeholder': 'Add a public comment...',
                       'rows': '2',}),
        }
