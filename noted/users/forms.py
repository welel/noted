from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _

from users.models import User


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
