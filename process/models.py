from datetime import datetime

from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.


class Game(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='games')
    start_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        datestring = self.start_date.strftime("%Y-%m-%d %H:%M:%S")
        return "game (%s) [%s]" % (datestring, str(self.user))


class Round(models.Model):

    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='rounds')

    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now=True)
    total_time = models.FloatField(default=0)

    seed = models.IntegerField(blank=True, null=True)
    possibilities = models.TextField(blank=True, null=True)

    def __str__(self):
        return "round (%s) [%s, game (%s)]" % (str(self.seed), str(self.game.user), str(self.game.start_date))

    def calculate_total_time(self):
        n = timezone.now()
        delta = n - self.start_date
        self.total_time = delta.total_seconds()
        return self.total_time

    def save(self, *args, **kwargs):
        if self.start_date:
            self.calculate_total_time()
        return super().save(args, kwargs)


class Step(models.Model):

    parent_round = models.ForeignKey(Round, on_delete=models.CASCADE, related_name='steps')

    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now=True)
    total_time = models.FloatField(blank=True, null=True)

    seed = models.IntegerField(blank=True, null=True)

    player_choice = models.TextField(blank=True, null=True)
    real_values = models.TextField(blank=True, null=True)
    cost = models.FloatField(blank=True, null=True)
    risk = models.FloatField(blank=True, null=True)
    expected_profit = models.FloatField(blank=True, null=True)
    expected_return = models.FloatField(blank=True, null=True)
    real_profit = models.FloatField(blank=True, null=True)
    real_return = models.FloatField(blank=True, null=True)

    def __str__(self):
        values = (str(self.seed), str(self.parent_round.game.user),
            str(self.parent_round.game.start_date), str(self.parent_round.seed))
        return "step (%s) [%s, game (%s), round (%s)]" % values

    def calculate_total_time(self):
        n = timezone.now()
        delta = n - self.start_date
        self.total_time = delta.total_seconds()
        return self.total_time

    def save(self, *args, **kwargs):
        if self.start_date:
            self.calculate_total_time()
        return super().save(args, kwargs)
