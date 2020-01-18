from django.contrib import admin
from django.db import models
from django.forms import Textarea

# Register your models here.

from .models import Game, Round, Step


class RoundInline(admin.StackedInline):
    model = Round
    extra = 0

class StepInline(admin.StackedInline):
    model = Step
    extra = 0
    fields = (('total_time', 'seed'), 'player_choice',
        ('expected_profit', 'expected_return'),
        ('real_profit', 'real_return'))
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':1, 'cols':40})},
    }
    # exclude = ('real_values', )

class GameAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'start_date', 'pk')
    inlines = [RoundInline, ]

class RoundAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'start_date', 'total_time', 'seed', 'pk')
    inlines = [StepInline, ]

    def user(self, obj):
        return str(obj.game.user)

class StepAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'start_date', 'total_time', 'round_seed', 'seed', 'pk')
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':1, 'cols':40})},
    }

    def user(self, obj):
        return str(obj.parent_round.game.user)

    def round_seed(self, obj):
        return str(obj.parent_round.seed)

admin.site.register(Game, GameAdmin)
admin.site.register(Round, RoundAdmin)
admin.site.register(Step, StepAdmin)