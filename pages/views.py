# -*- coding: UTF-8 -*-

import csv
from datetime import datetime

from django.http import HttpResponse
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
            record['end_date'] = step.end_date.strftime("%Y-%m-%d %H:%M:%S")
            for key in copy_names:
                try:
                    record[key[0]] = key[1] % getattr(step, key[0])
                except Exception as e:
                    record[key[0]] = getattr(step, key[0])
            result.append(record)

        return result

class DataCollector(object):

    data = []
    headers = [
        ['player', 'parent_round.game.user.username'],
        ['player id', 'parent_round.game.user.id'],
        ['game id', 'parent_round.game.id'],
        ['game start date', 'parent_round.game.start_date'],
        ['round id', 'parent_round.id'],
        ['round start date', 'parent_round.start_date'],
        ['round end date', 'parent_round.end_date'],
        ['round total time', 'parent_round.total_time'],
        ['round seed', 'parent_round.seed'],
        ['step id', 'id'],
        ['step start date', 'start_date'],
        ['step end date', 'end_date'],
        ['step total time', 'total_time'],
        ['step seed', 'seed'],
        ['player choice', 'player_choice'],
        ['real values', 'real_values'],
        ['cost', 'cost'],
        ['risk', 'risk'],
        ['expected profit', 'expected_profit'],
        ['expected return', 'expected_return'],
        ['real profit', 'real_profit'],
        ['real return', 'real_return'],
        ['player gender', 'parent_round.game.user.gender'],
        ['player experience', 'parent_round.game.user.experience'],
    ]


    def __init__(self):
        super(DataCollector, self).__init__()
        self.data = []
        return

    def collect_headers(self, result):
        row = []
        for h in self.headers:
            row.append(h[0])
        result.append(row)
        return result

    def map_value(self, value):
        if type(value) is datetime:
            return value.strftime("%Y-%m-%d %H:%M:%S.%f")
        return str(value)

    def collect_value(self, record, path):
        splitted = path.split(".")
        v = record
        for s in splitted:
            v = getattr(v, s)
        v = self.map_value(v)
        return v

    def collect_row(self, result, record):
        row = []
        for h in self.headers:
            row.append(self.collect_value(record, h[1]))
        result.append(row)
        return result

    def collect(self):
        result = []
        self.collect_headers(result)

        s = Step.objects.filter(seed__isnull=False)
        s = s.order_by("-end_date")
        for record in s:
            self.collect_row(result, record)

        self.data = result
        return result

    def export_to_csv(self, response):
        writer = csv.writer(response)
        for row in self.data:
            writer.writerow(row)
        return writer

def export_view(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="games_export.csv"'

    dc = DataCollector()
    dc.collect()
    dc.export_to_csv(response)

    return response
        