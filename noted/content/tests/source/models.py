from django.test import TestCase
from django.urls import reverse

from content.models import Source


class SourceModelTest(TestCase):
    def setUp(self):
        self.source = Source.objects.create(
            title="War and Peace", type=Source.BOOK
        )
        self.source_def_type = Source.objects.create(title="Car Manual")

    def test_defiend_type(self):
        self.assertEqual(self.source.type, "1")

    def test_default_type(self):
        self.assertEqual(self.source_def_type.type, Source.DEFAULT)

    def test_title_require(self):
        self.assertRaises(ValueError, Source.objects.create, type=Source.BOOK)

    def test_default_description(self):
        self.assertEqual(self.source.description, "")

    def test_default_link(self):
        self.assertEqual(self.source.link, "")

    def test_slug(self):
        self.assertIsNotNone(self.source.slug)

    def test_unique_slug(self):
        source2 = Source.objects.create(
            title="War and Peace", type=Source.BOOK
        )
        self.assertNotEqual(self.source.slug, source2.slug)

    def test_str(self):
        self.assertEqual(str(self.source), self.source.title)

    def test_reabable_type(self):
        self.assertEqual(Source.make_type_readable("1"), "Book")

    def test_reabable_type_none(self):
        self.assertIsNone(Source.make_type_readable("100"))

    def test_verbose_type(self):
        self.assertEqual(self.source.verbose_type, "Book")

    def test_url(self):
        self.assertIsNotNone(self.source.get_absolute_url())

    def test_type_url(self):
        self.assertIsNotNone(reverse("content:source_type", args=["1"]))

    def test_search(self):
        # PostgreSQL extenstion problem.
        pass
