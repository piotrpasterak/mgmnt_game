

from json import loads

from django.http import HttpResponseBadRequest, JsonResponse
from django.views.generic import TemplateView

from process.models import Round, Game
from .tools.game_engine import GameEngine, RoundEngine,\
        StepEngine, WalletCalculationsEngine

class PostTemplateView(TemplateView):

    def get(self, request, *args, **kwargs):
        return HttpResponseBadRequest('Bad GET request!')

    def post(self, request, *args, **kwargs):
        self.map_variables(request)

        context = self.get_context_data()
        rendered = self.render_to_response(context)
        return rendered

    def map_variables(self, request):
        p = dict(request.POST)

        prohibited_keys = []
        if hasattr(self, 'checkbox_name'):
            prohibited_keys.append(self.checkbox_name)
        if hasattr(self, 'projects_list'):
            prohibited_keys.append(self.projects_list)

        for key in p.keys():
            if type(p[key]) is list:
                if key in prohibited_keys:
                    continue
                p[key] = p[key][0]

        self.post = p
        return p


class InitGame(PostTemplateView):
    # this class creates game object and round 1
    template_name = "game/init_game.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        ge = GameEngine()
        g =ge.init_game(self.request.user)
        context['game'] = g
        context['game_id'] = g.id

        re = RoundEngine(g)
        r = re.init_round()
        context['round'] = r
        context['round_id'] = r.id
        context['round_data'] = loads(r.possibilities)
        context['round_iterator'] = list(range(1, context['round_data']['projekty']+1))

        se = StepEngine(r)
        s = se.blank_step()
        context['step'] = s
        context['step_id'] = s.id

        return context


class RoundSubmit(PostTemplateView):
    # this class is finishing the round
    checkbox_name = 'fields[]'
    template_name = "game/submit_round.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        se = StepEngine(self.post['roundId'])
        se.fill_step(self.post['stepId'], self.post[self.checkbox_name])

        context['game_id'] = se.ro.game_id
        context['round'] = se.ro
        context['round_id'] = se.ro.id
        context['round_data'] = loads(se.ro.possibilities)
        context['round_iterator'] = list(range(1, context['round_data']['projekty']+1))
        context['results'] = list(map(int, list(se.krok.zysk_rz)))

        # new step begin

        se = StepEngine(se.ro)
        s = se.blank_step()
        context['step'] = s
        context['step_id'] = s.id
        

        self.add_checkboxes_to_context(context)

        return context

    def add_checkboxes_to_context(self, context):
        if self.checkbox_name not in self.post:
            return context
        checkboxes = []
        for itr in range(context['round_data']['projekty']):
            name = str(itr)
            if name in self.post[self.checkbox_name]:
                checkboxes.append(" checked")
            else:
                checkboxes.append(" ")

        context['checkboxes'] = checkboxes

        return context


class InitRound(PostTemplateView):
    # this class creates round to known game
    template_name = "game/init_round.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        g = Game.objects.get(id=self.post['gameId'])
        context['game'] = g
        context['game_id'] = g.id

        re = RoundEngine(context['game'])
        r = re.init_round()
        context['round'] = r
        context['round_id'] = r.id
        context['round_data'] = loads(r.possibilities)
        context['round_iterator'] = list(range(1, context['round_data']['projekty']+1))

        se = StepEngine(r)
        s = se.blank_step()
        context['step'] = s
        context['step_id'] = s.id

        return context


class WalletCalculations(PostTemplateView):
    template_name = "game/wallet.html"
    projects_list = "chosen_projects[]"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        projects0 = [int(x) for x in self.post[self.projects_list]] # list of chosen projects, origin 0
        projects = [int(x)+1 for x in self.post[self.projects_list]] # list of chosen projects, origin 1
        context['projects'] = projects

        wc = WalletCalculationsEngine(self.post['round_id'])
        data = wc.calculate_values(projects0)
        for key in data.keys():
            context[key] = data[key]

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
