from django.test import TestCase, Client
from django.urls import reverse

from content.models import Source, Note
from users.models import User


class NoteModelTest(TestCase):
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

    def test_title_require(self):
        self.assertRaises(ValueError, Note.objects.create)

    def test_slug(self):
        self.assertEqual(self.note.slug, "some-note")

    def test_unique_slug(self):
        note = Note.objects.create(
            title="Some note",
            author=self.author,
        )
        self.assertNotEqual(note.slug, self.note.slug)

    def test_author_null_on_delete(self):
        author = User.objects.create(email="test@email.com", full_name="Name")
        note = Note.objects.create(title="note", author=author)
        author.delete()
        self.assertIsNone(Note.objects.get(pk=note.pk).author)

    def test_source_null_on_delete(self):
        source = Source.objects.create(type="1", title="Test")
        note = Note.objects.create(title="note", source=source)
        source.delete()
        self.assertIsNone(Note.objects.get(pk=note.pk).source)

    def test_bodyhtml(self):
        # Create valid test considering that 2 various results may occur
        pass

    def test_summary_default(self):
        self.assertEqual(self.note_only_title.summary, "")

    def test_draft_default(self):
        self.assertEqual(self.note.draft, False)

    def test_pin_default(self):
        self.assertEqual(self.note.pin, False)

    def test_datetime(self):
        pass

    def test_views_default(self):
        self.assertEqual(self.note.views, 0)

    def test_views(self):
        Client().get(reverse("content:note", args=[self.note.slug]))
        note = Note.objects.get(pk=self.note.pk)
        self.assertEqual(note.views, 1)

    def test_fork_null_on_delete(self):
        note = Note.objects.create(title="test")
        fork = Note.objects.create(title="test", fork=note)
        self.assertEqual(fork.fork, note)
        note.delete()
        self.assertIsNone(Note.objects.get(pk=fork.pk).fork)

    def test_note_str(self):
        self.assertEqual(str(self.note), self.note.title)

    def test_get_url(self):
        self.assertIsNotNone(self.note.get_absolute_url())

    def test_preview_text(self):
        self.assertEqual(self.note.get_preview_text(3), "Hel")

    def test_first_image_url_none(self):
        self.assertIsNone(self.note.first_image_url)

    def test_first_image_url(self):
        self.note_only_title.body_html = '<img src="image_url" />'
        self.assertEqual(self.note_only_title.first_image_url, "image_url")

    def test_md_file(self):
        file = self.note.generate_md_file()
        rows = file.read().decode().split("\n")
        self.assertEqual(rows[0], "# Some note")
        self.assertEqual(rows[-1], "# Hello")

    def test_html_file(self):
        file = self.note.generate_html_file()
        html = file.read().decode()
        self.assertEqual(html[:6], "<html>")
        self.assertEqual(html[-7:], "</html>")

    def test_pdf_file(self):
        file = self.note.generate_pdf_file()
        pdf = file.read()
        # How to decode?
        pass

    def test_generate_file_none(self):
        self.assertIsNone(self.note.generate_file(filetype="txt"))

    def test_generate_file(self):
        self.assertIsNotNone(self.note.generate_file())

    def test_generate_file_to_response(self):
        file = self.note.generate_file_to_response()
        self.assertIsNotNone(file["file"])
        self.assertEqual(file["filename"], self.note.slug + ".md")
        self.assertEqual(file["content_type"], "text/markdown; charset=UTF-8")

    def test_get_fork(self):
        fork = self.note.get_fork()
        self.assertEqual(fork.title, self.note.title)
        self.assertEqual(fork.source, self.note.source)
        self.assertEqual(fork.body_raw, self.note.body_raw)
        self.assertEqual(fork.body_html, self.note.body_html)
        self.assertEqual(fork.summary, self.note.summary)
        self.assertEqual(fork.tags, self.note.tags)
        self.assertEqual(fork.fork, self.note)
        self.assertEqual(fork.slug, "")
        self.assertIsNone(fork.author)
        self.assertFalse(fork.draft)
        self.assertFalse(fork.pin)
        self.assertFalse(fork.anonymous)
        self.assertEqual(fork.views, 0)

    def test_get_similar_by_tags(self):
        pass

    def test_this_year(self):
        pass

    def test_is_modified(self):
        pass

    def test_min_read(self):
        pass
