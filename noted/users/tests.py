import json

import django
from django.core.signing import TimestampSigner
from django.test import Client, TestCase

from users.models import User, SignupToken, UserManager


class URLTests(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ajax_client = Client(HTTP_X_REQUESTED_WITH="XMLHttpRequest")

    def test_signup_request(self):
        response = self.ajax_client.post(
            "/en/users/signup-request/",
            {"email": "non@existing.email"},
            content_type="application/json",
        )
        answer = json.loads(response.content)["msg"]
        self.assertEqual(answer, "sent")

    def test_email_validation_free(self):
        response = self.ajax_client.get(
            "/en/users/validate-email/",
            {"email": "free@email.qq"},
        )
        answer = json.loads(response.content)["is_taken"]
        self.assertEqual(answer, False)

    def test_email_validation_taken(self):
        User.objects.create(email="taken@email.qq")
        response = self.ajax_client.get(
            "/en/users/validate-email/",
            {"email": "taken@email.qq"},
        )
        answer = json.loads(response.content)["is_taken"]
        self.assertEqual(answer, True)

    def test_signup_bad_token(self):
        response = self.ajax_client.get("/en/users/signup/asjdk21d/")
        self.assertEqual(response.status_code, 302)

    def test_signup_good_token(self):
        signer = TimestampSigner()
        stoken = signer.sign("some@email.qq")
        token = SignupToken.objects.create(token=stoken)
        response = self.ajax_client.get(f"/en/users/signup/{token.token}/")
        self.assertEqual(response.context.get("error"), None)
        self.assertEqual(response.status_code, 200)

    def test_signin_success(self):
        user = User.objects.create(
            username="@some.name",
            full_name="Some Name",
            email="some@email.qq",
        )
        user.set_password("easypass123")
        user.save()
        response = self.ajax_client.post(
            "/en/users/signin/",
            {"email": user.email, "password": "easypass123"},
            content_type="application/json",
        )
        code = json.loads(response.content)["code"]
        self.assertEqual(code, "success")

    def test_signin_noemail_error(self):
        response = self.ajax_client.post(
            "/en/users/signin/",
            {"email": "non@existing.email", "password": "easypass123"},
            content_type="application/json",
        )
        code = json.loads(response.content)["code"]
        self.assertEqual(code, "noemail")

    def test_signin_bad_password_error(self):
        user = User.objects.create(
            username="@some.name",
            full_name="Some Name",
            email="some@email.qq",
            password="one_pass",
        )
        response = self.ajax_client.post(
            "/en/users/signin/",
            {"email": user.email, "password": "wrong_pass"},
            content_type="application/json",
        )
        code = json.loads(response.content)["code"]
        self.assertEqual(code, "badpass")

    def test_signin_bad_request(self):
        response = self.client.get("/en/users/signin/")
        self.assertEqual(response.status_code, 400)

    def test_signout(self):
        response = self.client.get("/en/users/signout/")
        self.assertEqual(response.status_code, 302)


class ModelsTests(TestCase):
    def test_username_generator_unique(self):
        username = User.objects._generate_username("Some Name")
        self.assertEqual(username, "@some.name")

    def test_username_generator_taken(self):
        user = User.objects.create(email="one_email", full_name="Some Name")
        user.save()
        user2 = User.objects.create(
            email="another_email", full_name="Some Name"
        )
        user2.save()
        self.assertEqual(user2.username, "@some.name2")

    def test_username_generator_full_name_empty(self):
        user = User.objects.create()
        self.assertRaises(ValueError, User.objects._generate_username, "")

    def test_email_exists(self):
        User.objects.create(email="email")
        self.assertRaises(
            django.db.utils.IntegrityError, User.objects.create, email="email"
        )

    def test_user_str(self):
        user = User.objects.create(email="email", full_name="some name")
        self.assertEqual(str(user), "@some.name / email")

    def test_user_url(self):
        user = User.objects.create(email="email", full_name="some name")
        self.assertEqual(user.get_absolute_url(), "/users/some-name/")

    def test_signup_token_creates(self):
        pass

    def test_signup_token_deletes(self):
        pass

    def test_signup_token_expires(self):
        pass

    def test_signup_token_doesnt_exists(self):
        pass
