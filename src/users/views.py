from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView

from common.view import TitleMixin
from users.forms import RegistrationQueryForm, UserLoginForm
from users.models import RegistrationQueries, User


class IndexView(TitleMixin, TemplateView):
    template_name = 'index.html'
    title = 'R4C'


class UserLoginView(TitleMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    redirect_authenticated_user = True
    title = 'R4C - Авторизация'

    def form_invalid(self, form):
        res = super().form_invalid(form)
        return res


class RegistrationView(SuccessMessageMixin, TitleMixin, CreateView):
    model = RegistrationQueries
    form_class = RegistrationQueryForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/registration.html'
    success_message = 'После проверки администратора, на вашу почту придут данные для входа'
    title = 'R4C - Регистрация'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            form.add_error('email', 'Пользователь с таким email уже существует.')
            return self.form_invalid(form)
        elif RegistrationQueries.objects.filter(email=email).exists():
            form.add_error('email', 'Ваш запрос уже принят на рассмотрение.')
            return self.form_invalid(form)
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        return super().get(request, *args, **kwargs)
