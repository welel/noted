from django.test import Client, TestCase
from django.urls import reverse

from content.models import Source


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
