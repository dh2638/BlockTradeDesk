# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import views
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView
from django.views.generic import TemplateView

from _utils.views import AjaxableResponseMixin, LoginRequiredMixin
from accounts import forms


class LoginView(AjaxableResponseMixin, views.LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    form_class = forms.LoginForm
    success_message = _('You have successfully logged in')


class SignUpView(AjaxableResponseMixin, FormView):
    template_name = 'accounts/signup.html'
    form_class = forms.SignUpForm
    success_message = _('Your account successfully created')
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        form.save()
        return super(SignUpView, self).form_valid(form)


class LogoutView(views.LogoutView):
    pass


class ChangePasswordView(AjaxableResponseMixin, views.PasswordChangeView):
    success_url = '/'
    template_name = 'accounts/password_change_form.html'
    form_class = forms.PasswordChangeForm
    success_message = _('Successfully chnaged password')


class ResetPasswordView(AjaxableResponseMixin, views.PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    form_class = forms.PasswordResetForm
    email_template_name = 'accounts/password_reset_email.html'
    success_url = '/'
    success_message = _('We sent you an email. Please confirm your email')


class PasswordResetConfirmView(AjaxableResponseMixin, views.PasswordResetConfirmView):
    form_class = forms.SetPasswordForm
    success_url = reverse_lazy('accounts:login')
    success_message = _('Successfully reset your password')
    template_name = 'accounts/password_reset_confirm.html'


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'


class ProfileEditView(AjaxableResponseMixin, LoginRequiredMixin, FormView):
    template_name = 'accounts/profile_edit.html'
    form_class = forms.ProfileUpdateForm
    success_message = _('Profile updated successfully')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileEditView, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(ProfileEditView, self).get_form_kwargs()
        kwargs.update({'instance': self.request.user})
        return kwargs
