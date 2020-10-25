from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, PasswordChangeView
from .forms import RegistrationForm, LoginForm, AccountChangeForm, ImageForm
from django.contrib import messages
from .ConfirmEmail import confirm
from .models import InfoUser


@login_required
def account(request):
    return render(request, 'account/account.html')


class LoginAccount(LoginView):
    template_name = 'account/login.html'
    form_class = LoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, "Вход выполнен успешно")
        return super(LoginAccount, self).form_valid(form)


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            image = InfoUser()
            image.user = user
            image.save()
            confirm(request, user)
            messages.success(request, "Регистрация прошла успешно. "
                                      "Пожалуйста, подтвердите свой адрес электронной почты, "
                                      "чтобы завершить регистрацию")

            if request.user.is_authenticated:
                logout(request)
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'account/registration.html', {'form': form})


@login_required()
def account_edit(request):
    if request.method == 'POST':
        form_image = ImageForm(request.POST, request.FILES)
        form = AccountChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Редактирование прошло успешно')
        if form_image.is_valid():
            image = InfoUser.objects.get(user=request.user)
            image.image = request.FILES['image']
            image.save()
            messages.success(request, 'Аватарка изменена')
    else:
        form = AccountChangeForm(instance=request.user)
        form_image = ImageForm()
    return render(request, 'account/account_edit.html', {'form': form, 'form_image': form_image})


class PasswordChangeV(PasswordChangeView):
    success_url = reverse_lazy('account')

    def form_valid(self, form):
        messages.success(self.request, 'Пароль изменен')
        return super(PasswordChangeV, self).form_valid(form)
