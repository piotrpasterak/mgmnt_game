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
    step = ""
    seed = 0

    def __init__(self, round_id):
        super(StepEngine, self).__init__()
        self.ro = Round.objects.get(pk=round_id)
        self.init_step()
        return

    def init_step(self):
        seed = randint(0, settings.MAX_SEED)
        self.seed = seed

        # initializing objects
        runda = Runda(self.ro.seed)
        runda.rozpakuj_dane(self.ro.possibilities)

        krok = Krok(runda, seed)
        self.step = krok

        # saving to database
        self.save_step()
        return

    def save_step(self):
        step = Step()
        step.parent_round = self.ro
        step.seed = self.seed
        step.player_choice = ""
        step.real_values = dumps(list(map(int, self.step.sprz_rz)))
        step.save()

