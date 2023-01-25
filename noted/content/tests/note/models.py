import datetime

from django.test import Client, TestCase
from django.urls import reverse

from content.models import Note, Source
from users.models import User


class NoteModelTest(TestCase):
    def setUp(self):
        self.source = Source.objects.create(
            title="War and Peace", type=Source.BOOK
        )
        self.source2 = Source.objects.create(
            title="Hello world Java", type=Source.TUTORIAL
        )
        self.author = User.objects.create(
            email="user@email.qq", full_name="Some User"
        )
        self.author2 = User.objects.create(
            email="user2@email.qq", full_name="Some User Two"
        )
        self.note = Note.objects.create(
            title="Some note",
            author=self.author,
            body_raw="# Hello",
            summary="Greeting",
            source=self.source,
        )
        self.note.tags.add("literature")
        self.note_only_title = Note.objects.create(title="xyz")
        self.note_draft = Note.objects.create(
            title="note", draft=True, author=self.author, source=self.source
        )
        self.note_anon = Note.objects.create(
            title="note", anonymous=True, author=self.author
        )
        self.note_anon.tags.add("money")
        self.note_pin = Note.objects.create(
            title="note", pin=True, author=self.author2, source=self.source2
        )
        self.note_pin.likes.add(self.author)
        self.note_most_liked = Note.objects.create(title="note")
        self.note_most_liked.likes.add(self.author)
        self.note_most_liked.likes.add(self.author2)
        # self.note_most_liked.save
        self.note_pin.tags.add("dev")
        self.note_high_views = Note.objects.create(title="note", views=100)
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

    def test_get_similar_by_tags_in(self):
        similar_tag_note = Note.objects.create(title="1984")
        similar_tag_note.tags.add("literature")
        similar_tag_note.save()
        self.assertIn(similar_tag_note, self.note.get_similar_by_tags())

    def test_get_similar_by_tags_not_in(self):
        not_similar_tag_note = Note.objects.create(title="YouTube")
        not_similar_tag_note.tags.add("youtube")
        not_similar_tag_note.save()
        self.assertNotIn(not_similar_tag_note, self.note.get_similar_by_tags())

    def test_this_year_false(self):
        self.note_only_title.modified -= datetime.timedelta(days=365)
        self.assertFalse(self.note_only_title.this_year)

    def test_this_year_true(self):
        self.assertTrue(self.note_only_title.this_year)

    def test_is_modified_true(self):
        self.note_only_title.created -= datetime.timedelta(days=1)
        self.assertTrue(self.note_only_title.is_modified)

    def test_is_modified_false(self):
        self.assertFalse(self.note_only_title.is_modified)

    def test_min_read(self):
        self.note.body_raw = "s" * 1000
        self.assertEqual(self.note.min_read, 1)

    def test_min_read_2(self):
        self.note.body_raw = "s" * 5000
        self.assertEqual(self.note.min_read, 5)

    def test_manager_public(self):
        personal = Note.objects.personal(self.author)
        self.assertIn(self.note, personal)
        self.assertIn(self.note_draft, personal)
        self.assertIn(self.note_anon, personal)
        # self.note_pin.author != self.author
        self.assertNotIn(self.note_pin, personal)

    def test_manager_profile(self):
        profile = Note.objects.profile(self.author)
        self.assertIn(self.note, profile)
        self.assertNotIn(self.note_draft, profile)
        self.assertNotIn(self.note_anon, profile)
        # self.note_pin.author != self.author
        self.assertNotIn(self.note_pin, profile)

    def test_manager_public(self):
        public = Note.objects.public()
        self.assertIn(self.note, public)
        self.assertNotIn(self.note_draft, public)
        self.assertIn(self.note_anon, public)
        self.assertIn(self.note_pin, public)

    def test_manager_created(self):
        self.assertEqual(
            list(reversed(Note.objects.by_created()))[0], self.note
        )
        # last created
        self.assertEqual(Note.objects.by_created()[0], self.note_high_views)

    def test_manager_with_source_type(self):
        qs = Note.objects.with_source_type(Source.BOOK)
        self.assertNotIn(self.note_draft, qs)
        self.assertIn(self.note, qs)
        self.assertNotIn(self.note_pin, qs)

    def test_manager_popular(self):
        popular = Note.objects.popular()
        self.assertEqual(popular[0], self.note_high_views)

    def test_manager_most_liked(self):
        most_liked = Note.objects.most_liked()
        self.assertEqual(most_liked[0], self.note_most_liked)
        self.assertEqual(most_liked[1], self.note_pin)
        self.assertNotIn(self.note_draft, most_liked)
        self.assertIn(self.note, most_liked)

    def test_manager_tags_in(self):
        tagged = Note.objects.tags_in(["money", "dev"])
        self.assertIn(self.note_pin, tagged)
        self.assertIn(self.note_anon, tagged)
        self.assertNotIn(self.note, tagged)

    def test_manager_tags_in_not_duplicates(self):
        note = Note.objects.create(title="title")
        note.tags.add("tag1", "tag2")
        self.assertEqual(len(Note.objects.tags_in(["tag1", "tag2"])), 1)

    def test_manager_search(self):
        # PostrgreSQL extension problem
        pass
