from django.test import Client, TestCase
from django.urls import reverse

from .models import CoachingRequest, ToolSignup


class WebsiteTests(TestCase):
    def setUp(self):
        self.url = reverse("website:home")

    def test_home_renders_both_forms(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "website/home.html")
        self.assertContains(response, "Treava V. Barnes")
        self.assertIn("lead_form", response.context)
        self.assertIn("contact_form", response.context)

    def test_signup_is_saved_and_email_is_normalized(self):
        response = self.client.post(
            self.url, {"form_type": "lead", "email": " Stylist@Example.COM "}
        )
        self.assertRedirects(response, self.url + "#free", fetch_redirect_response=False)
        self.assertEqual(ToolSignup.objects.get().email, "stylist@example.com")

    def test_duplicate_signup_does_not_create_another_record(self):
        ToolSignup.objects.create(email="stylist@example.com")
        response = self.client.post(
            self.url, {"form_type": "lead", "email": "STYLIST@example.com"}, follow=True
        )
        self.assertEqual(ToolSignup.objects.count(), 1)
        self.assertContains(response, "already registered")

    def test_invalid_signup_keeps_errors_without_saving(self):
        response = self.client.post(self.url, {"form_type": "lead", "email": "invalid"})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context["lead_form"], "email", "Enter a valid email address.")
        self.assertEqual(ToolSignup.objects.count(), 0)

    def test_coaching_request_is_saved(self):
        response = self.client.post(
            self.url,
            {
                "form_type": "contact",
                "name": "Salon Creative",
                "email": "creative@example.com",
                "topic": CoachingRequest.Topic.PRICING,
                "message": "I need help setting my service prices.",
            },
        )
        self.assertRedirects(response, self.url + "#contact", fetch_redirect_response=False)
        saved = CoachingRequest.objects.get()
        self.assertEqual(saved.name, "Salon Creative")
        self.assertEqual(saved.topic, CoachingRequest.Topic.PRICING)
        self.assertEqual(saved.message, "I need help setting my service prices.")

    def test_invalid_coaching_request_is_not_saved(self):
        response = self.client.post(
            self.url,
            {"form_type": "contact", "name": "", "email": "bad", "topic": "unknown"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("name", response.context["contact_form"].errors)
        self.assertIn("email", response.context["contact_form"].errors)
        self.assertIn("topic", response.context["contact_form"].errors)
        self.assertEqual(CoachingRequest.objects.count(), 0)

    def test_coaching_message_is_optional(self):
        response = self.client.post(
            self.url,
            {
                "form_type": "contact",
                "name": "Salon Creative",
                "email": "creative@example.com",
                "topic": CoachingRequest.Topic.OTHER,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(CoachingRequest.objects.get().message, "")

    def test_post_requires_csrf_token(self):
        client = Client(enforce_csrf_checks=True)
        response = client.post(self.url, {"form_type": "lead", "email": "stylist@example.com"})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(ToolSignup.objects.count(), 0)

    def test_unknown_form_does_not_save(self):
        response = self.client.post(self.url, {"email": "stylist@example.com"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(ToolSignup.objects.count(), 0)
        self.assertEqual(CoachingRequest.objects.count(), 0)

    def test_admin_requires_login(self):
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login/", response.url)
