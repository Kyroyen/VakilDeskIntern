from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination

from .serializers import OscarFilmsSerializer, HockeyTeamsSerializer
from .models import HockeyTeams, OscarFilms

class HockeyTeamsView(APIView, LimitOffsetPagination):

    def get(self, request):
        hockey_items = HockeyTeams.objects.all()
        results = self.paginate_queryset(hockey_items, request, view = self)
        # print(results)
        serializer = HockeyTeamsSerializer(results, many = True)
        return self.get_paginated_response(serializer.data)
    
class OscarFilmsView(APIView, LimitOffsetPagination):
    
    def get(self, request):
        oscar_items = OscarFilms.objects.all()
        results = self.paginate_queryset(oscar_items, request, view = self)
        serializer = OscarFilmsSerializer(results, many = True)
        return self.get_paginated_response(serializer.data)

