from json import loads, dumps
from random import randint

from django.conf import settings

from process.models import Game, Round, Step

from .portfolio import Runda

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
        
