from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from hostel.models import Hostel, Payments, Student, Visitor, Warden, room


class StudentFormTests(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            username="manager",
            password="test-password-123",
            is_staff=True,
        )
        self.client.force_login(user)

    def test_submitted_student_is_saved_and_shown_in_table(self):
        response = self.client.post(
            reverse("student_form"),
            {
                "first_name": "Amina",
                "last_name": "Nabirye",
                "email": "amina@example.com",
                "birth_date": "2004-05-12",
                "no_of_courses": "3",
                "gender": "F",
                "hostel": "",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Student.objects.count(), 1)
        self.assertContains(response, "Student added successfully.")
        self.assertContains(response, "Amina")
        self.assertContains(response, "Nabirye")
        self.assertContains(response, "amina@example.com")
        self.assertContains(response, "3")
        self.assertContains(response, "Female")

    def test_all_management_pages_can_add_records(self):
        cases = [
            ("students", Student, {
                "first_name": "Amina", "last_name": "Nabirye",
                "email": "amina@example.com", "birth_date": "2004-05-12",
                "no_of_courses": "3", "gender": "F", "hostel": "",
            }),
            ("hostels", Hostel, {
                "name": "Sunrise", "address": "Kampala", "total_rooms": "20",
                "location": "Central",
            }),
            ("wardens", Warden, {
                "first_name": "John", "last_name": "Okello",
                "email": "john@example.com", "gender": "M", "hostel": "",
            }),
            ("rooms", room, {
                "room_number": "12", "capacity": "4", "hostel": "", "status": "A",
            }),
            ("payments", Payments, {
                "student": "", "amount": "50000.00", "make_payment": "on",
                "reason": "Hostel fees",
            }),
            ("visitors", Visitor, {
                "visitor_name": "Grace Namusoke", "phone_number": "0700000000",
                "student": "", "purpose": "Family visit",
            }),
        ]

        for entity, model, data in cases:
            with self.subTest(entity=entity):
                response = self.client.post(reverse("entity_manage", args=(entity,)), data)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(model.objects.count(), 1)

    def test_visitor_records_can_be_edited_and_deleted(self):
        visitor = Visitor.objects.create(
            visitor_name="Grace Namusoke",
            phone_number="0700000000",
            purpose="Family visit",
        )

        response = self.client.post(
            reverse("entity_edit", args=("visitors", visitor.pk)),
            {
                "visitor_name": "Grace N.",
                "phone_number": "0711111111",
                "student": "",
                "purpose": "Updated visit",
            },
        )
        self.assertEqual(response.status_code, 200)
        visitor.refresh_from_db()
        self.assertEqual(visitor.visitor_name, "Grace N.")

        response = self.client.post(reverse("entity_delete", args=("visitors", visitor.pk)))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Visitor.objects.exists())


class AuthenticationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_superuser(
            username="test-admin",
            email="admin@example.com",
            password="test-admin-password-456",
        )

    def test_management_pages_require_sign_in(self):
        response = self.client.get(reverse("student_form"))
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('student_form')}",
        )

    def test_admin_can_sign_in_and_sign_out(self):
        response = self.client.post(
            reverse("login"),
            {"username": "test-admin", "password": "test-admin-password-456"},
        )
        self.assertRedirects(response, reverse("index_view"))
        self.assertEqual(self.client.get(reverse("student_form")).status_code, 200)

        response = self.client.post(reverse("logout"))
        self.assertRedirects(response, reverse("index_view"))
        self.assertRedirects(
            self.client.get(reverse("student_form")),
            f"{reverse('login')}?next={reverse('student_form')}",
        )
