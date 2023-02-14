from django.core.exceptions import FieldDoesNotExist
from django.http import HttpRequest, HttpResponseBadRequest
from django.test import TestCase

from content.models import Source
from users.models import User

from .decorators import ajax_required
from .text import generate_unique_slug, transcript_ru2en, is_latin


class Tests(TestCase):
    def test_unique_slug_generator(self):
        source = Source(title="War and Peace", type=Source.BOOK)
        slug = generate_unique_slug(source, "title", "slug")
        self.assertEqual(slug, "war-and-peace")

    def test_unique_slug_generator_uniqueness(self):
        source = Source.objects.create(title="War and Peace", type=Source.BOOK)
        source2 = Source(title="War and Peace", type=Source.BOOK)
        slug = generate_unique_slug(source2, "title", "slug")
        self.assertNotEqual(source.slug, slug)

    def test_unique_slug_generator_nonexisting_field(self):
        source = Source(title="War and Peace", type=Source.BOOK)
        self.assertRaises(
            FieldDoesNotExist,
            generate_unique_slug,
            source,
            "not_exists",
            "slug",
        )

    def test_unique_slug_generator_empty(self):
        source = Source(title="", type=Source.BOOK)
        self.assertRaises(ValueError, generate_unique_slug, source)

    def test_ajax_required(self):
        @ajax_required()
        def view(request):
            return True

        request = Source()
        request.headers = {"X-Requested-With": "XMLHttpRequest"}
        self.assertTrue(view(request))

    def test_ajax_required_not_ajax(self):
        @ajax_required()
        def view(request):
            return True

        request = HttpRequest()
        request.user = User.objects.first()
        self.assertIsInstance(view(request), HttpResponseBadRequest)

    def test_transcript_ru2en(self):
        self.assertEqual(transcript_ru2en("Привет, миръ!"), "Privet, mir!")
        self.assertEqual(
            transcript_ru2en(
                "Транслитерация русского текста на английский язык."
            ),
            "Transliteracia russkogo teksta na angliiskii azik.",
        )

    def test_is_latin_with_latin_word(self):
        self.assertTrue(is_latin("Hello"))

    def test_is_latin_with_non_latin_word(self):
        self.assertFalse(is_latin("Привет"))

    def test_is_latin_with_mixed_word(self):
        self.assertFalse(is_latin("Hello мир"))

    def test_is_latin_with_empty_word(self):
        self.assertTrue(is_latin(""))
