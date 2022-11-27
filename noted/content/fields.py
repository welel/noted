from simplemde.fields import SimpleMDEField

from django.db.models import TextField

from content.markdown import pick_markdown_to_html


class RenderedMarkdownField(TextField):
    """
    RenderedMarkdownField is just html code in plain/text format.
    """

    def __init__(self, *args, **kwargs):
        kwargs["editable"] = False
        kwargs["blank"] = False
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["editable"]
        return name, path, args, kwargs


class MarkdownField(SimpleMDEField):
    def __init__(self, *args, rendered_field: str = None, **kwargs):
        self.rendered_field = rendered_field
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.rendered_field is not None:
            kwargs["rendered_field"] = self.rendered_field
        return name, path, args, kwargs

    def pre_save(self, model_instance, add):
        value = super().pre_save(model_instance, add)

        if not self.rendered_field:
            return value

        html = pick_markdown_to_html(value)
        setattr(model_instance, self.rendered_field, html)

        return value
