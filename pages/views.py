# -*- coding: UTF-8 -*-

from django.views.generic import TemplateView

from process.models import Game, Round, Step

class GameView(TemplateView):
    template_name = "game/main.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class ResultsView(TemplateView):
    template_name = "results.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['games'] = self.restore_history()        

        return context

    def restore_history(self):
        user_pk = self.request.user.pk
        result = []

        # find games
        g = Game.objects.filter(user_id=user_pk)
        g = g.order_by('-start_date')
        for game in g:
            record = {}
            record['start_date'] = game.start_date.strftime("%Y-%m-%d %H:%M:%S")
            record['children'] = self.restore_history_rounds(game.id)
            record['rowspan'] = 0
            if len(record['children']) > 0:
                # do not append empty game
                for child in record['children']:
                    record['rowspan'] += child['rowspan']
                result.append(record)

        return result

    def restore_history_rounds(self, game_id):
        result = []

        r = Round.objects.filter(game_id=game_id)
        r = r.order_by('-start_date')

        for ro in r:
            record = {}
            record['start_date'] = ro.start_date.strftime("%Y-%m-%d %H:%M:%S")
            record['end_date'] = ro.end_date.strftime("%Y-%m-%d %H:%M:%S")
            record['total_time'] = "%.2f" % ro.total_time
            record['children'] = self.restore_history_steps(ro.id)
            record['rowspan'] = len(record['children'])
            if record['rowspan'] > 0:
                # do not append empty round
                result.append(record)

        return result

    def restore_history_steps(self, round_id):
        result = []

        s = Step.objects.filter(parent_round_id=round_id).filter(total_time__gte=0)
        s = s.order_by('-start_date')

        copy_names = [['total_time', "%.2f"], ['cost', "%d"], ['risk', "%.2f"],
            ['expected_profit', "%d"], ['expected_return', "%.3f"],
            ['real_profit', "%d"], ['real_return', "%.3f"]]

        for step in s:
            record = {}
            record['start_date'] = step.start_date.strftime("%Y-%m-%d %H:%M:%S")
            record['end_date'] = step.start_date.strftime("%Y-%m-%d %H:%M:%S")
            for key in copy_names:
                try:
                    record[key[0]] = key[1] % getattr(step, key[0])
                except Exception as e:
                    record[key[0]] = getattr(step, key[0])
            result.append(record)

        return result