# -*- coding: UTF-8 -*-

from django.views.generic import TemplateView

class GameView(TemplateView):
    template_name = "game/main.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class ResultsView(TemplateView):
    template_name = "results.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.request)
        print(kwargs)
        return context