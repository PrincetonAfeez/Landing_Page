"""Tests for the project."""

from django.test import TestCase
from django.urls import reverse

from pages.content import SITE_NAME


class PublicPagesTests(TestCase):
    def test_home_ok(self):
        response = self.client.get(reverse("pages:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, SITE_NAME)

    def test_robots_txt_absolute_sitemap(self):
        response = self.client.get(reverse("robots_txt"))
        self.assertEqual(response.status_code, 200)
        body = response.content.decode()
        self.assertIn("Sitemap: http://testserver/sitemap.xml", body)

    def test_sitemap_xml(self):
        response = self.client.get(reverse("sitemap"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<urlset", response.content)
        self.assertIn(b"http://testserver/", response.content)

    def test_open_graph_card_png(self):
        response = self.client.get(reverse("pages:og_card"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("png", response["Content-Type"].lower())
        self.assertTrue(response.content.startswith(b"\x89PNG\r\n\x1a\n"))
