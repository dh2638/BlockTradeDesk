from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import password_validation, authenticate
from django.utils.translation import ugettext_lazy as _, ugettext

from _utils.forms import DictErrorMixin
from .models import UserAccount


class LoginForm(DictErrorMixin, forms.Form):
    email = forms.EmailField(max_length=254, label=_('Email address'))
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput, )

    error_messages = {
        'invalid_login': _(
            "Please enter a correct %(email)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email is not None and password:
            self.user_cache = authenticate(self.request, username=email, password=password)
            if self.user_cache is None:
                try:
                    self.user_cache = UserAccount._default_manager.get_by_natural_key(email)
                except UserAccount.DoesNotExist:
                    pass
                else:
                    self.confirm_login_allowed(self.user_cache)
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'email': email},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache


class SignUpForm(DictErrorMixin, forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    required_fields = ['first_name', 'last_name', 'email']

    class Meta:
        model = UserAccount
        fields = ('first_name', 'last_name', 'email', 'password',)

    def save(self, commit=True):
        confirm_password = self.cleaned_data.pop('confirm_password')
        user = super(SignUpForm, self).save(commit=False)
        user.set_password(confirm_password)
        if commit:
            user.save()
        return user

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError(ugettext("The two password fields didn't match."))
        password_validation.validate_password(self.cleaned_data.get('confirm_password'))
        return confirm_password


class PasswordChangeForm(DictErrorMixin, auth_forms.PasswordChangeForm):
    pass


class SetPasswordForm(DictErrorMixin, auth_forms.SetPasswordForm):
    pass


class PasswordResetForm(DictErrorMixin, auth_forms.PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not UserAccount._default_manager.filter(email=email).exists():
            raise forms.ValidationError(ugettext('This email not exist'))
        return email


class ProfileUpdateForm(DictErrorMixin, forms.ModelForm):
    class Meta:
        model = UserAccount
        fields = ('first_name', 'last_name',)
