from django.contrib import admin

from .models import OscarFilms, HockeyTeams, HeaderSpoofResponse

admin.site.register(OscarFilms)
admin.site.register(HockeyTeams)
admin.site.register(HeaderSpoofResponse)