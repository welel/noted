import re

from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _

from users.models import User, UserProfile


def validate_username(username: str):
    """Validates username.

    Min length = 5
    Max length = 150
    Username starts with '@' sign.
    """
    if 5 > len(username) or len(username) > 150:
        raise ValidationError(
            _(
                f"Username should contain less than 150 symbols \
                    and more than 4."
            )
        )
    if username[0] != "@":
        raise ValidationError(_("Username should start with '@' sign."))
    if not re.fullmatch(
        r"^@([a-zA-Z]+\.[a-zA-Z]+\.?)+[a-zA-Z]+\d*$", username
    ):
        raise ValidationError(
            _(
                "Username can't start or end with a dot. Two dots can't be \
                next to each other. Digits can be added only at the end."
            )
        )


def validate_full_name(full_name: str):
    """Validates full name."""
    if not full_name:
        raise ValidationError(_("Full name can't be empty."))
    if not full_name.replace(" ", "").isalpha():
        raise ValidationError(_("Full name should contain only letters."))
    if len(full_name.split()) > 3:
        raise ValidationError(_("Full name should contain less than 3 words."))


def validate_social_username(username: str):
    """Validates full name."""
    if "?" in username:
        raise ValidationError(_("Username should not contain '?' sign."))
    if len(username) > 200:
        raise ValidationError(
            _("Username should contain less than 200 symbols.")
        )


class SignupForm(UserCreationForm):

    full_name = forms.CharField(
        max_length=50,
        min_length=3,
        widget=forms.TextInput(
            attrs={"class": "form-control", "autocomplete": "given-name"}
        ),
        strip=True,
        help_text=_(
            "Full Name should contain only latin letters, and \
                   should include no more than 3 words"
        ),
    )
    password1 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": "form-control"}
        ),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": "form-control"}
        ),
        strip=False,
    )

    class Meta:
        model = User
        fields = ("full_name",)

    def clean_full_name(self):
        data = self.cleaned_data["full_name"]
        if not data.replace(" ", "").isalpha():
            raise forms.ValidationError(
                _("Full Name should contain only latin letters.")
            )
        if len(data.split()) > 3:
            raise forms.ValidationError(
                _("Full Name should include no more than 3 words.")
            )
        return data


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "full_name")

        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control", "autocomplete": "username"}
            ),
            "full_name": forms.TextInput(
                attrs={"class": "form-control", "autocomplete": "name"}
            ),
        }

    def clean_username(self):
        # The form input field in without '@' sign.
        username = "@" + self.cleaned_data.get("username", "")
        validate_username(username)
        return username

    def clean_full_name(self):
        full_name = self.cleaned_data.get("full_name", "")
        validate_full_name(full_name)
        return full_name.title()


class UserProfileForm(forms.ModelForm):
    twitter = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    github = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    facebook = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = UserProfile
        fields = ("avatar", "bio", "location", "socials")

        widgets = {
            "bio": forms.Textarea(
                attrs={"class": "form-control", "rows": "5"}
            ),
            "location": forms.TextInput(
                attrs={"class": "form-control", "autocomplete": "country-name"}
            ),
        }

    def clean_twitter(self):
        twitter = self.cleaned_data.get("twitter", "")
        validate_social_username(twitter)
        return twitter.replace(" ", "")

    def clean_facebook(self):
        facebook = self.cleaned_data.get("facebook", "")
        validate_social_username(facebook)
        return facebook.replace(" ", "")

    def clean_github(self):
        github = self.cleaned_data.get("github", "")
        validate_social_username(github)
        return github.replace(" ", "")

    def clean(self):
        twitter = self.cleaned_data.get("twitter")
        facebook = self.cleaned_data.get("facebook")
        github = self.cleaned_data.get("github")
        self.cleaned_data[
            "socials"
        ] = '{"facebook": "%s", "twitter": "%s", "github": "%s"}' % (
            facebook,
            twitter,
            github,
        )
