from django.core.mail import send_mail, EmailMessage
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import render, redirect


def confirm(request, user):
    current_site = get_current_site(request)
    mail_subject = 'Активируйте свой аккаунт'
    message = render_to_string('account/acc_active_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user)
    })
    to_email = user.email
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Аккаунт был успешно акктивирован')
        return redirect('login')
    else:
        messages.error(request, 'Ссылка на активацию недействительна!')
        return redirect('beer')
