import django
from django.test import TestCase

from content.models import Source, Note
from users.models import User


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

    def test_defiend_sourcetype(self):
        self.assertEqual(self.source.type, "BOOK")

    def test_source_str(self):
        self.assertEqual(str(self.source), self.source.title)

    def test_source_slug(self):
        self.assertIsNotNone(self.source.slug)

    def test_source_url(self):
        pass

    def test_source_unique_slug(self):
        source2 = Source.objects.create(
            title="War and Peace", type=Source.BOOK
        )
        self.assertNotEqual(self.source.slug, source2.slug)

    def test_source_default_type(self):
        source = Source.objects.create(title="1984")
        self.assertEqual(source.type, Source.DEFAULT)

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
