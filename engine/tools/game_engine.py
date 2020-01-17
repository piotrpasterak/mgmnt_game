# -*- coding: UTF-8 -*-

from json import loads, dumps
from random import randint

from django.conf import settings

from process.models import Game, Round, Step

from .portfolio import Runda, Krok

class GameEngine(object):

    def __init__(self):
        super(GameEngine, self).__init__()
        return

    def init_game(self, user):
        new_game = Game()
        new_game.user = user
        new_game.save()
        return new_game
    
class RoundEngine(object):

    game = ""

    def __init__(self, game_id):
        super(RoundEngine, self).__init__()
        
        # finding and applying Game object
        if type(game_id) is int:
            # expecting Game object ID
            self.game = Game.object.get(pk=game_id)
        else:
            # expecting Game object directly
            self.game = game_id

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
        super(StepEngine, self).__init__()

        # finding and applying Round object
        if type(round_id) is int:
            # expecting Round object ID
            self.ro = Round.objects.get(pk=round_id)
        if type(round_id) is str:
            # expecting Round object ID as string
            self.ro = Round.objects.get(pk=int(round_id))
        else:
            # expecting Round object directly
            self.ro = round_id
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

