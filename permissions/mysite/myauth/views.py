from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, CreateView
from .models import Profile

class AboutMeView(TemplateView):
    template_name = "myauth/about-me.html"


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'myauth/register.html'
    success_url = reverse_lazy('myauth:about-me')

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(self.request, username=username, password=password)
        login(self.request, user=user)
        return response


def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/admin/')

        return render(request, 'myauth/login.html')

    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/admin/')
    return render(request, 'myauth/login.html', {'error': 'Invalid username or password'})


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect(reverse('myauth:login'))


class MyLogoutView(LogoutView):
    next_page = reverse_lazy('myauth:login')


