from taggit.forms import TagWidget
from mptt.forms import TreeNodeChoiceField
from mptt.querysets import TreeQuerySet

from django.core.exceptions import ValidationError
from django import forms

from notes.models import Note, Comment


class NoteForm(forms.ModelForm):

    class Meta:
        model = Note
        fields = ['title', 'source', 'private', 'anonymous', 'allow_comments',
                  'tags', 'body_raw', 'summary']
        widgets = {'tags': TagWidget(attrs={'data-role': 'tagsinput'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body_raw'].label = ''

    def clean_tags(self):
        """Validates the `tags` field.
        
        Validates the number of tags (less than 6) and tag length
        (less than 25 symbols).
        """
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
    """Comment Form for ``Comment`` model.

    The `parent` field is a selector field. It has all existing comments
    from database in options to select. It is a bad situation, because
    we want only root comments for one specific note. So we use
    a `comment_form_factory` function to handle this situation.

    TODO: Find a better way to reduce the number of comments in the form.
          May be to create own model for comments.

    """

    class Meta:
        model = Comment
        fields = ('parent', 'content',)
        widgets = {
            'content': forms.Textarea(
                attrs={'class': 'form-control shadow-none',
                    'placeholder': 'Add a public comment...',
                    'rows': '2',}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # `d-none` is Bootstrap class to hide an element.
        # `parent` field fills via JavaScript `static/js/comments.js`.
        self.fields['parent'].widget.attrs.update({'class': 'd-none'})
        self.fields['parent'].label = ''
        self.fields['parent'].required = False
        self.fields['content'].label = ''


def comment_form_factory(comments: TreeQuerySet) -> CommentForm:
    """A factory function for creating ``CommentForm``.
    
    ``CommentForm`` has a field `parent` that has all comments from database
    in options to select. The factory helps to reduce comments with given
    comments.

    Args:
        comments: a queryset of comments.

    Returns:
        New class ``CommentForm`` with modified a `parent` field.
    """
    class CommentFormModified(CommentForm):
        parent = TreeNodeChoiceField(queryset=comments)
    return CommentFormModified


class SearchForm(forms.Form):
    """A form for searching."""
    query = forms.CharField()
    query.widget.attrs.update({'placeholder': 'Search'})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['query'].label = ''
