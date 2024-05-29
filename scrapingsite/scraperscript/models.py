from django.db import models

class HockeyTeams(models.Model):

    team_name = models.CharField(max_length=50, null=True)
    year = models.SmallIntegerField(null=True)
    wins = models.IntegerField(null=True, blank=True)
    losses = models.SmallIntegerField(null=True, blank=True)
    ot_losses = models.CharField(max_length=50, null=True, blank=True)
    win_percent = models.FloatField(null=True, blank=True)
    goals_for = models.IntegerField(null=True, blank=True)
    goals_against = models.IntegerField(null=True, blank=True)
    plus_minus = models.IntegerField(null=True, blank=True)


class OscarFilms(models.Model):

    title = models.CharField(max_length=50)
    nominations = models.IntegerField(null=True, blank=True)
    awards = models.IntegerField(null=True, blank=True)
    best_picture = models.BooleanField(default=False, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
