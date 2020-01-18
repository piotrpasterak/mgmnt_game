# -*- coding: UTF-8 -*-

from json import loads, dumps
from random import randint

from django.conf import settings

from process.models import Game, Round, Step

from .portfolio import Runda, Krok


def find_object(klass, pk):
    if type(pk) is klass:
        # object itself
        return pk
    elif type(pk) is int:
        # object id as integer
        return klass.objects.get(pk=pk)
    elif type(pk) is str:
        # object id as string
        return klass.objects.get(pk=int(pk))
    # unknown object, return empty class
    return klass()


class GameEngine(object):

    def __init__(self):
        super().__init__()
        return

    def init_game(self, user):
        new_game = Game()
        new_game.user = user
        new_game.save()
        return new_game


class RoundEngine(object):

    game = ""

    def __init__(self, game_id):
        super().__init__()
        
        # finding and applying Game object
        self.game = find_object(Game, game_id)
        return

    def init_round(self):
        new_round = Round()
        new_round.game = self.game
        seed = randint(0, settings.MAX_SEED)
        new_round.seed = seed

        p = Runda(seed)
        new_round.possibilities = dumps(p.spakuj_dane())
        new_round.save()
        return new_round


class StepEngine(object):

    ro = "" # "round" jest zarezerwowane
    runda = ""
    step = ""
    krok = ""
    seed = 0

    def __init__(self, round_id):
        super().__init__()

        # finding and applying Round object
        self.ro = find_object(Round, round_id)
        return

    def blank_step(self):
        step = Step()
        step.parent_round = self.ro
        step.save()
        self.step = step
        return step

    def fill_step(self, step_id, player_choices):
        seed = randint(0, settings.MAX_SEED)
        self.seed = seed

        # initializing objects
        runda = Runda(self.ro.seed)
        runda.rozpakuj_dane(self.ro.possibilities)
        self.runda = runda

        krok = Krok(runda, seed)
        self.krok = krok

        # saving to database
        self.save_step(step_id, player_choices)
        self.ro.save()
        return krok

    def save_step(self, step_id, player_choices):
        step = Step.objects.get(id=step_id)
        step.seed = self.seed
        choices = list(map(int, player_choices))
        step.player_choice = dumps(choices)
        real_values = list(map(int, self.krok.sprz_rz))
        step.real_values = dumps(real_values)
        
        cost = 0
        for pr in choices:
            cost += self.runda.koszty[pr]
        step.cost = cost

        expected_profit = 0
        for pr in choices:
            expected_profit += self.runda.zyski[pr]
        step.expected_profit = expected_profit
        step.expected_return = expected_profit / cost

        real_profit = 0
        profits = list(map(int, self.krok.zysk_rz))
        for pr in choices:
            real_profit += profits[pr]
        step.real_profit = real_profit
        step.real_return = real_profit / cost

        step.save()

        self.step = step
        return step


class WalletCalculationsEngine(object):

    runda = ""
    ro = ""
    krok = ""
    step = ""

    def __init__(self, round_id, step_id=None):
        super().__init__()

        # finding and applying Round object
        self.ro = find_object(Round, round_id)

        # initializing objects
        runda = Runda(self.ro.seed)
        runda.rozpakuj_dane(self.ro.possibilities)
        self.runda = runda

        if step_id is not None:
            self.step = find_object(Step, step_id)
            self.krok = Krok(self.runda, self.step.seed)

        return

    def calculate_values(self, projects_list):
        result = {}
        cost = 0
        for pr in projects_list:
            cost += self.runda.koszty[pr-1]
        result['cost'] = cost

        expected_profit = 0
        for pr in projects_list:
            expected_profit += self.runda.zyski[pr-1]
        result['expected_profit'] = expected_profit
        expected_return = expected_profit / cost
        result['expected_return'] = "%.2f" % expected_return

        # RYzypor = np.round(np.average(self.runda.b, weights=self.runda.a), 2)
        # result['risk']
        risk = self.runda.oszacuj_ryzyko(projects_list)
        result['risk'] = "%.2f" % risk

        if self.krok != "":
            real_profit = 0
            for pr in projects_list:
                real_profit += self.krok.zysk_rz[pr]
            result['real_profit'] = real_profit
            real_return = real_profit / cost
            result['real_return'] = "%.2f" % real_return

        return result


        