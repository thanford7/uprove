from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import EmployerInterest
from ..utils.dateUtil import serializeDatetime


class EmployerInterestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # print(request.data)
        return Response(data={})
