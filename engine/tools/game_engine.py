from process.models import Game, Round, Step

from .portfolio import Projekty, Portfele, Wykresy

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
            game = Game.object.get(pk=game_id)
        else:
            # expecting Game object directly
            game = game_id


        return
        
