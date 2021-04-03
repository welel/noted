from django.test import TestCase

from notes.models import Note
from user.models import User


class NoteTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test_user', password='test')
        self.note = Note.objects.create(title='New TestNote', author=self.user)

    def test_slug(self):
        self.assertEqual(self.note.slug, 'new-testnote')

    def test_unique_slug(self):
        note_2 = Note.objects.create(title='New Test Note', author=self.user)
        self.assertNotEqual(self.note.slug, note_2.slug)
