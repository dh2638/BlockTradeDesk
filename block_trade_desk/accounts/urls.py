from django.conf.urls import url

from .views import (LoginView, SignUpView, LogoutView, ResetPasswordView,
                    ChangePasswordView, PasswordResetConfirmView, ProfileEditView, ProfileView)

urlpatterns = [
    url(r'^$', LoginView.as_view(), name='login'),
    url(r'^signup/$', SignUpView.as_view(), name='signup'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^profile/$', ProfileView.as_view(), name='profile_view'),
    url(r'^profile/edit/$', ProfileEditView.as_view(), name='profile_edit_view'),
    url(r'^password-reset/$', ResetPasswordView.as_view(), name='password_reset'),
    url(r'^password-change/$', ChangePasswordView.as_view(), name='password_change'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
