from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from upapp.models import Country, State


class LocationView(APIView):

    def get(self, request):
        return Response(status=status.HTTP_200_OK, data={
            'countries': [{'name': c.countryName, 'id': c.id} for c in Country.objects.all()],
            'states': [{'name': s.stateName, 'id': s.id} for s in State.objects.all()]
        })
