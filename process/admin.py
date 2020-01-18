from django.contrib import admin

# Register your models here.

from .models import Game, Round, Step


class RoundInline(admin.StackedInline):
    model = Round
    extra = 0

class StepInline(admin.StackedInline):
    model = Step
    extra = 0
    fields = ('total_time', 'player_choice',
        ('expected_profit', 'expected_return'),
        ('real_profit', 'real_return'))
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
    pass

admin.site.register(Game, GameAdmin)
admin.site.register(Round, RoundAdmin)
admin.site.register(Step, StepAdmin)