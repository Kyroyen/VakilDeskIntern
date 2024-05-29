from rest_framework.serializers import ModelSerializer

from .models import HockeyTeams, OscarFilms


class HockeyTeamsSerializer(ModelSerializer):
    class Meta:
        model = HockeyTeams
        fields = [
            "id",
            "year",
            "wins",
            "losses",
            "ot_losses",
            "win_percent",
            "goals_for",
            "goals_against",
            "plus_minus",
        ]
        extra_kwargs = {
            "id" : {
                "read_only" : True,
            }
        }

class OscarFilmsSerializer(ModelSerializer):
    class Meta:
        model = OscarFilms
        fields = "__all__"
        extra_kwargs = {
            "id" : {
                "read_only" : True,
            }
        }
