# -*- coding: UTF-8 -*-

from django.http import HttpResponseBadRequest, JsonResponse
from django.views.generic import TemplateView


class PostTemplateView(TemplateView):

    def get(self, request, *args, **kwargs):
        return HttpResponseBadRequest('Bad GET request!')

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        rendered = self.render_to_response(context)
        return rendered


class InitGame(PostTemplateView):
    # this class creates game object and round 1
    template_name = "game/init_game.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        

        return context

class InitRound(PostTemplateView):
    # this class creates round to known game
    template_name = "game/init_round.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class ProjectView(PostTemplateView):
    # this class creates single project plot
    template_name = "game/project_plot.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class WalletAnalysisView(PostTemplateView):
    # this class is plotting wallet analysis
    template_name = "game/wallet_plot.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class RoundSubmit(PostTemplateView):
    # this class is finishing the round
    template_name = "game/submit_round.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
