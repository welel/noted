import json
from pathlib import Path
from unittest import skip
from unittest.mock import Mock


import django
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.signing import TimestampSigner
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.utils import timezone

from .models import AuthToken, Following
from .validators import (
    validate_image,
    validate_username,
    validate_full_name,
    validate_social_username,
)


User = get_user_model()


class URLTests(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ajax_client = Client(HTTP_X_REQUESTED_WITH="XMLHttpRequest")

    @skip("Celery: connection resued.")
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
        self.assertEqual(response.status_code, 200)

    def test_signup_good_token(self):
        signer = TimestampSigner()
        stoken = signer.sign("some@email.qq")
        token = AuthToken.objects.create(token=stoken, type=AuthToken.SIGNUP)
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


class UserModelTest(TestCase):
    def setUp(self):
        self.mark = User.objects.create(
            email="watney@nasa.us",
            full_name="Mark Watney",
            password="spacepirate543",
        )
        self.beth = User.objects.create(
            email="johanssen@nasa.us", full_name="Beth Johanssen"
        )
        self.rich = User.objects.create(email="purnell@nasa.us")

    def test_username_generator_unique(self):
        self.assertEqual(self.mark.username, "@mark.watney")

    def test_username_generator_taken(self):
        mark2 = User.objects.create(
            email="watney2@nasa.us",
            full_name="Mark Watney",
            password="spacepirate543",
        )
        mark3 = User.objects.create(
            email="watney3@nasa.us",
            full_name="Mark Watney",
            password="spacepirate543",
        )
        self.assertEqual(mark2.username, "@mark.watney2")
        self.assertEqual(mark3.username, "@mark.watney3")

    def test_username_generator_empty_str(self):
        self.assertRaises(ValueError, User.objects._generate_username, "")

    def test_username_generator_latin(self):
        self.assertEqual(
            User.objects._generate_username("Jordan Piterson"),
            "@jordan.piterson",
        )

    def test_username_generator_slav(self):
        self.assertEqual(
            User.objects._generate_username("Лев Толстой"),
            "@lev.tolstoi",
        )

    def test_email_exists(self):
        self.assertRaises(
            django.db.utils.IntegrityError,
            User.objects.create,
            email="watney@nasa.us",
        )

    def test_user_str(self):
        self.assertEqual(str(self.mark), "@mark.watney")

    def test_user_url(self):
        self.assertEqual(
            self.mark.get_absolute_url(), "/en/u/notes/mark-watney/"
        )


class UserProfileModelTest(TestCase):
    def setUp(self):
        self.mark = User.objects.create(
            email="watney@nasa.us",
            full_name="Mark Watney",
            password="spacepirate543",
        )

    def test_user_default_avatar_exists(self):
        self.assertTrue(Path(self.mark.profile.avatar.path).is_file())

    def test_user_default_avatar_path(self):
        self.assertEqual(
            self.mark.profile.avatar, settings.DEFAULT_USER_AVATAR_PATH
        )

    def test_user_default_socials(self):
        instance_socials = list(self.mark.profile.socials.keys())
        default_socials = ["facebook", "twitter", "github"]
        self.assertListEqual(instance_socials, default_socials)


class ValidatorsTest(TestCase):
    def test_validate_image(self):
        image = Mock()
        image.file.size = 513 * 1024
        self.assertRaises(ValidationError, validate_image, image)

    def test_validate_username_not_str(self):
        self.assertRaises(ValidationError, validate_username, 12)

    def test_validate_username_short_len(self):
        self.assertRaises(ValidationError, validate_username, "@na")

    def test_validate_username_long_len(self):
        self.assertRaises(ValidationError, validate_username, "@name" * 40)

    def test_validate_username_miss_sign(self):
        self.assertRaises(ValidationError, validate_username, "mark.wantey")

    def test_validate_username_next_dots(self):
        self.assertRaises(ValidationError, validate_username, "@mark..wantey")

    def test_validate_username_digit_inside(self):
        # Allows on end `@mark.watney2`
        self.assertRaises(ValidationError, validate_username, "@2mark.wantey")
        self.assertRaises(ValidationError, validate_username, "@mark2.wantey")
        self.assertRaises(ValidationError, validate_username, "@mark.2wantey")
        self.assertRaises(ValidationError, validate_username, "@mark.wan2tey")

    def test_validate_full_name_empty(self):
        self.assertRaises(ValidationError, validate_full_name, "")

    def test_validate_full_name_not_alpha(self):
        self.assertRaises(ValidationError, validate_full_name, "Mark Watney2")

    def test_validate_full_name_max_len(self):
        # Allows 3 and less
        self.assertRaises(
            ValidationError, validate_full_name, "One Two Three Four"
        )

    def test_validate_social_usernames_question_sign(self):
        self.assertRaises(
            ValidationError, validate_social_username, "watney?q=hack"
        )

    def test_validate_social_usernames_max_len(self):
        self.assertRaises(ValidationError, validate_social_username, "s" * 201)


class FollowingModelTest(TestCase):
    def setUp(self):
        self.mark = User.objects.create(
            email="watney@nasa.us", full_name="Mark Watney"
        )
        self.beth = User.objects.create(
            email="johanssen@nasa.us", full_name="Beth Johanssen"
        )
        self.following = Following.objects.create(
            follower=self.mark, followed=self.beth
        )

    def test_str_method(self):
        self.assertEqual(
            str(self.following), f"{self.mark} follows {self.beth}"
        )

    def test_created_field(self):
        self.assertIsNotNone(self.following.created)

    def test_ordering(self):
        user3 = User.objects.create(email="testuser3@email.com")
        following2 = Following.objects.create(
            follower=self.mark, followed=user3
        )
        following3 = Following.objects.create(
            follower=self.beth, followed=user3
        )
        followings = Following.objects.all()
        self.assertEqual(followings[0], following3)
        self.assertEqual(followings[1], following2)
        self.assertEqual(followings[2], self.following)

    def test_manager_methods(self):
        following_qs = self.beth.followers.all()
        self.assertEqual(following_qs.count(), 1)
        self.assertEqual(following_qs[0], self.following)


class AuthTokenTest(TestCase):
    def test_auth_token_str(self):
        token = AuthToken.objects.create(token="abc123", type=AuthToken.SIGNUP)
        self.assertEqual(str(token), f"{token.token} ({token.type})")

    def test_auth_token_get_from_str(self):
        signup_token = AuthToken.objects.create(
            token="abc123", type=AuthToken.SIGNUP
        )
        change_email_token = AuthToken.objects.create(
            token="def456", type=AuthToken.CHANGE_EMAIL
        )

        # Test that we can get a token with the correct type and token string
        retrieved_token = AuthToken.get_from_str(
            signup_token.token, AuthToken.SIGNUP
        )
        self.assertEqual(retrieved_token, signup_token)

        # Test that we can't get a token with the wrong type
        with self.assertRaises(AuthToken.DoesNotExist):
            AuthToken.get_from_str(signup_token.token, AuthToken.CHANGE_EMAIL)

        # Test that we can't get a token with the wrong token string
        with self.assertRaises(AuthToken.DoesNotExist):
            AuthToken.get_from_str("wrong_token_string", AuthToken.SIGNUP)

    def test_auth_token_auto_now_add(self):
        now = timezone.now()
        token = AuthToken.objects.create(token="abc123", type=AuthToken.SIGNUP)
        self.assertLessEqual(
            token.created - now, timezone.timedelta(seconds=1)
        )
