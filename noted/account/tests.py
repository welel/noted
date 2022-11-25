import json

from django.core.signing import TimestampSigner
from django.test import Client, TestCase

from account.auth import generate_username
from account.models import User, SignupToken
from account.exceptions import FirstNameDoesNotSetError


class URLTests(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ajax_client = Client(HTTP_X_REQUESTED_WITH="XMLHttpRequest")

    def test_signup_request(self):
        response = self.ajax_client.post(
            "/en/account/signup-request/",
            {"email": "non@existing.email"},
            content_type="application/json",
        )
        answer = json.loads(response.content)["msg"]
        self.assertEqual(answer, "sent")

    def test_email_validation_free(self):
        response = self.ajax_client.get(
            "/en/account/validate-email/",
            {"email": "free@email.qq"},
        )
        answer = json.loads(response.content)["is_taken"]
        self.assertEqual(answer, False)

    def test_email_validation_taken(self):
        User.objects.create(email="taken@email.qq")
        response = self.ajax_client.get(
            "/en/account/validate-email/",
            {"email": "taken@email.qq"},
        )
        answer = json.loads(response.content)["is_taken"]
        self.assertEqual(answer, True)

    def test_signup_bad_token(self):
        response = self.ajax_client.get("/en/account/signup/asjdk21d/")
        self.assertEqual(response.status_code, 302)

    def test_signup_good_token(self):
        signer = TimestampSigner()
        stoken = signer.sign("some@email.qq")
        token = SignupToken.objects.create(token=stoken)
        response = self.ajax_client.get(f"/en/account/signup/{token.token}/")
        self.assertEqual(response.context.get("error"), None)
        self.assertEqual(response.status_code, 200)

    def test_signin_success(self):
        user = User.objects.create(
            username="@some.name",
            first_name="Some Name",
            email="some@email.qq",
            password="easypass123",
        )
        response = self.ajax_client.post(
            "/en/account/signin/",
            {"email": user.email, "password": user.password},
            content_type="application/json",
        )
        code = json.loads(response.content)["code"]
        self.assertEqual(code, "success")

    def test_signin_noemail_error(self):
        response = self.ajax_client.post(
            "/en/account/signin/",
            {"email": "non@existing.email", "password": "easypass123"},
            content_type="application/json",
        )
        code = json.loads(response.content)["code"]
        self.assertEqual(code, "noemail")

    def test_signin_bad_password_error(self):
        user = User.objects.create(
            username="@some.name",
            first_name="Some Name",
            email="some@email.qq",
            password="one_pass",
        )
        response = self.ajax_client.post(
            "/en/account/signin/",
            {"email": user.email, "password": "wrong_pass"},
            content_type="application/json",
        )
        code = json.loads(response.content)["code"]
        self.assertEqual(code, "badpass")

    def test_signin_bad_request(self):
        response = self.client.get("/en/account/signin/")
        self.assertEqual(response.status_code, 400)


class AuthUtilsTests(TestCase):
    def test_username_generator_unique(self):
        user = User.objects.create(first_name="Some Name")
        username = generate_username(user)
        self.assertEqual(username, "@some.name")

    def test_username_generator_taken(self):
        user = User.objects.create(first_name="Some Name")
        user.username = generate_username(user)
        user.save()
        user2 = User(first_name="Some Name")
        username = generate_username(user2)
        self.assertEqual(username, "@some.name2")

    def test_username_generator_first_name_empy(self):
        user = User.objects.create()
        self.assertRaises(FirstNameDoesNotSetError, generate_username, user=user)
