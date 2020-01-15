# -*- coding: UTF-8 -*-

from json import loads

from django.http import HttpResponseBadRequest, JsonResponse
from django.views.generic import TemplateView

from .tools.game_engine import GameEngine, RoundEngine

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

        ge = GameEngine()
        context['game'] = ge.init_game(self.request.user)
        context['game_id'] = context['game'].id

        re = RoundEngine(context['game'])
        r = re.init_round()
        context['round'] = r
        context['round_data'] = loads(r.possibilities)
        context['round_iterator'] = list(range(1, 1+context['round_data']['projekty']))

        print(context)

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
