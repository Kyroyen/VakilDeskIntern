from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from .serializers import OscarFilmsSerializer, HockeyTeamsSerializer
from .models import HockeyTeams, OscarFilms
from .single_event_scraper import advanced_header_spoofing

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
    
class AdvancedHeaderView(APIView):

    def get(self, request):
        message = "Successful" if advanced_header_spoofing() else "Failed"
        return Response({"message": f"Advanced Header Spoofing {message}"})
    
