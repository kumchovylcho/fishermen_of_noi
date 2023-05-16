from django.shortcuts import render
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'home.html'


class WelcomePageView(TemplateView):
    template_name = 'welcome-page.html'
