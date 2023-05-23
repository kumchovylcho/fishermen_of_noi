from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'home.html'


class WelcomePageView(TemplateView):
    template_name = 'welcome-page.html'


class PageNotFound(TemplateView):
    template_name = '404.html'

    def dispatch(self, request, *args, **kwargs):
        return HttpResponseNotFound(render(request, self.get_template_names()), status=404)