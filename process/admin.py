from django.contrib import admin

# Register your models here.

from .models import Game, Round, Step


class RoundInline(admin.StackedInline):
    model = Round
    extra = 0

class GameAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'start_date', 'pk')
    inlines = [RoundInline, ]

class RoundAdmin(admin.ModelAdmin):
    pass

class StepAdmin(admin.ModelAdmin):
    pass

admin.site.register(Game, GameAdmin)
admin.site.register(Round, RoundAdmin)
admin.site.register(Step, StepAdmin)