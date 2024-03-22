from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import CalculationResult, CalculationResultYear


class ViewTestCase(TestCase):
    def test_display_index(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_display_registration(self):
        response = self.client.get(reverse("registration"))
        self.assertEqual(response.status_code, 200)

    def test_register_user(self):
        username = "john_smith"
        password = "abcdabcd"

        self.assertFalse(User.objects.filter(username=username).exists())

        response = self.client.post(
            reverse("registration"),
            {
                "username": username,
                "password1": password,
                "password2": password,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username=username).exists())
        self.assertRedirects(response, reverse("login"))


# Add new tests for CalculationResult and CalculationResultYear


class CalculationResultTestCase(TestCase):
    def test_submit_calculation_result(self):
        # Assuming 'calculate_tax' requires a user to be logged in
        user = User.objects.create_user(username="testuser", password="12345")
        self.client.login(username="testuser", password="12345")

        form_data = {
            "zakladni_mzda": 10000,
            "prirazky": 0,
            "slevy": ["poplatnik"],  # Change as per your actual form fields
            "deti": "bezdětný",
            "invalidita": "bezinvalidity",
            "ztp": "bez",
        }

        response = self.client.post(reverse("calculate_tax"), form_data)
        self.assertEqual(response.status_code, 200)  # Redirects after successful post
        self.assertTrue(CalculationResult.objects.filter(user=user).exists())


class CalculationResultYearTestCase(TestCase):
    def test_submit_yearly_calculation_result(self):
        # Assuming 'calculate_tax_rok' requires a user to be logged in
        user = User.objects.create_user(username="testuser2", password="12345")
        self.client.login(username="testuser2", password="12345")

        form_data = {
            "zakladni_mzda1": 120000,
            "slevy1": ["poplatnik"],  # Change as per your actual form fields
            "deti1": "bezdětný",
            "invalidita1": "bezinvalidity",
            "ztp1": "bez",
        }

        response = self.client.post(reverse("calculate_tax2"), form_data)
        self.assertEqual(response.status_code, 200)  # Redirects after successful post
        self.assertTrue(CalculationResultYear.objects.filter(user=user).exists())
