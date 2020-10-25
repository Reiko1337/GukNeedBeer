from django.urls import path
from .views import account, LoginAccount, registration, account_edit, PasswordChangeV
from .ConfirmEmail import activate
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView, PasswordChangeView, PasswordChangeDoneView
from .forms import PasswordReset, SetPassword, PasswordChange

urlpatterns = [
    path('', account, name='account'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginAccount.as_view(), name='login'),
    path('registration/', registration, name='registration'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('account_edit/', account_edit, name='account_edit'),

    path('password_reset/',
         PasswordResetView.as_view(form_class=PasswordReset, template_name='account/password_reset_form.html'),
         name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(form_class=SetPassword, template_name='account/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'),
         name='password_reset_complete'),

    path('password_change/',
         PasswordChangeV.as_view(form_class=PasswordChange, template_name='account/password_change.html'),
         name='password_change'),
]
