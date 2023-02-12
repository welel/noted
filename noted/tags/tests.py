from django.test import TestCase

from .utils import custom_tag_string


class CustomTagStringTest(TestCase):
    def test_empty_string(self):
        result = custom_tag_string("")
        self.assertEqual(result, [])

    def test_single_tag(self):
        result = custom_tag_string("python")
        self.assertEqual(result, ["python"])

    def test_multiple_tags_separated_by_comma(self):
        result = custom_tag_string("python, django, unit test")
        self.assertEqual(result, ["python", "django", "unit-test"])

    def test_multiple_tags_separated_by_space(self):
        result = custom_tag_string("python django unit test")
        self.assertEqual(result, ["python-django-unit-test"])

    def test_mixed_separator(self):
        result = custom_tag_string("python,django unit test")
        self.assertEqual(result, ["python", "django-unit-test"])
