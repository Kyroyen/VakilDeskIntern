from django.urls import path
from .views import HockeyTeamsView, OscarFilmsView, AdvancedHeaderView

urlpatterns = [
    path('hockey-teams/', HockeyTeamsView.as_view(), name = "hockey-teams"),
    path('oscar-films/', OscarFilmsView.as_view(), name = "oscar-films"),
    path("advanced-header/", AdvancedHeaderView.as_view(), name="advanced-header"),
]