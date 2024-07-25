from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
# Create your views here.


@api_view()
def home(request):
    return Response({'status': 200, 'message': 'Hello from django rest framework'})


class RegisterUser(APIView):
    def post(self,request):
        pass
