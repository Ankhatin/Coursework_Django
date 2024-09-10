import secrets
import string
import random

from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, TemplateView

from users.forms import UserRegisterForm
from users.models import User


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(8)
        host = self.request.get_host()
        user.token = token
        user.save()
        url = f'http://{host}/users/email-confirm/{token}'
        send_to = form.cleaned_data['email']
        send_mail('Верификация почты',
                  f'Подтвердите свою электронную почту {url}',
                  None,
                  [send_to],
                  fail_silently=False)
        return super().form_valid(form)


class UserListView(LoginRequiredMixin, TemplateView):
    template_name = 'users/user_list.html'
    login_url = "/users/login"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        user = self.request.user
        block = context_data['view'].request.GET.get("block")
        unblock = context_data['view'].request.GET.get("unblock")
        if block and user.has_perm('users.can_ban_user'):
            pk = block
            user_to_ban = User.objects.get(pk=pk)
            user_to_ban.is_active = False
            user_to_ban.save()
        elif unblock and user.has_perm('users.can_ban_user'):
            pk = unblock
            user_to_unban = User.objects.get(pk=pk)
            user_to_unban.is_active = True
            user_to_unban.save()
        context_data['object_list'] = User.objects.exclude(is_staff=True)
        return context_data


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = get_object_or_404(User, email=email)
        characters = string.ascii_letters + string.digits
        password = ''.join(random.choice(characters) for i in range(8))
        user.password = make_password(password)
        user.save()
        send_mail('Сброс пароля',
                  f'Ваш новый пароль {password}',
                  None,
                  [user.email],
                  fail_silently=False)
        return redirect(reverse('users:login'))
    return render(request, 'users/reset_password.html')
