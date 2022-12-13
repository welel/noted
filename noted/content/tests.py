import django
from django.test import TestCase, Client
from django.urls import reverse

from content.models import Source, Note
from users.models import User


##########
# MODELS #
##########


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

    def test_get_readable_type(self):
        self.assertEqual(self.source.get_readable_type(), "Book")

    def test_url(self):
        self.assertIsNotNone(self.source.get_absolute_url())

    def test_type_url(self):
        self.assertIsNotNone(reverse("content:source_type", args=["1"]))


class ModelsTest(TestCase):
    def setUp(self):
        self.source = Source.objects.create(
            title="War and Peace", type=Source.BOOK
        )
        self.source_def_type = Source.objects.create(title="Car Manual")
        self.author = User.objects.create(
            email="user@email.qq", full_name="Some User"
        )
        self.note = Note.objects.create(
            title="Some note",
            author=self.author,
            body_raw="# Hello",
            summary="Greeting",
        )
        self.note_only_title = Note.objects.create(title="xyz")
        return super().setUp()

    def test_note_str(self):
        self.assertEqual(str(self.note), self.note.title)

    def test_note_unique_slug(self):
        note = Note.objects.create(
            title="Some note",
            author=self.author,
            body_raw="# Hello",
            summary="Greeting",
        )
        self.assertNotEqual(note.slug, self.note.slug)

    def test_note_author_null(self):
        self.assertIsNone(self.note_only_title.author)

    def test_note_source_null(self):
        self.assertIsNone(self.note_only_title.source)

    def test_note_bodyraw_empty(self):
        self.assertEqual(self.note_only_title.body_raw, "")

    def test_note_bodyhtml_empty(self):
        pass
        # TODO: create valid test considering that 2 various results may occur
        # self.assertEqual(self.note_only_title.body_html, "")

    def test_note_summary_empty(self):
        self.assertEqual(self.note_only_title.summary, "")

    def test_note_bodyhtml(self):
        pass
        # TODO: create valid test considering that 2 various results may occur
        # self.assertHTMLEqual(
        #     self.note.body_html,
        #     "<h1><a id='user-content-hello' class='anchor' aria-hidden='true' href='#hello'><span aria-hidden='true' class='octicon octicon-link'></span></a>Hello</h1>",
        # )

    def test_note_datetime(self):
        self.note.title += "mod"
        self.assertNotEqual(self.note.created, self.note.modified)


########
# URLS #
########


class SourceUrlsTest(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ajax_client = Client(HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.client = Client()

    def setUp(self):
        self.source = Source.objects.create(
            type=Source.BOOK,
            title="War and Peace",
            link="http://warandpeace.ru",
            description="Great book!",
        )
        return super().setUp()

    def test_search_source_ajax(self):
        # PostgreSQL extenstion problem.
        pass

    def test_source_details(self):
        response = self.client.get(
            reverse("content:source", args=[self.source.slug])
        )
        self.assertEqual(response.status_code, 200)

    def test_source_type_details(self):
        response = self.client.get(
            reverse("content:source_type", args=[Source.BOOK])
        )
        self.assertEqual(response.status_code, 200)
