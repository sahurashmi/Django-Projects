
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . models import sports
from . serializers import sportsSerializer
        

class SportListView(APIView):                  # inherits from an APIView
 
    def get(self, request):
        obj = sports.objects.all()      # Getting all values
        serializer = sportsSerializer(obj, many=True)
        return Response(serializer.data, status=200)
    
    def post(self, request):
        data = request.data             # Data passed in body
        serializer = sportsSerializer(data=data)  
        if serializer.is_valid(raise_exception=True):
            name= serializer.validated_data.get('name')
            sport= serializer.validated_data.get('sport')
            age= serializer.validated_data.get('age')
            sport_id = sports.objects.create(name=name, age=age, sport=sport)
            return Response("Record Inserted !!!!!!")
       


class SportDetailView(APIView):    # Handle entry-specific operations
 
    def get(self, request, id=None):
        try:
            data = sports.objects.get(id=id)
            return Response(sportsSerializer(data).data, status=200)
        except sports.DoesNotExist:
            return Response({"Error":"sport {} does not exist.".format(id)})
    def put(self, request, id=None):
        data = request.data             # Data passed in body
        serializer = sportsSerializer(data=data)  
        if serializer.is_valid(raise_exception=True):
            try:
                #breakpoint()
                serializer_data = serializer.validated_data
                data = sports.objects.get(id=id)
                data.name =serializer_data.get('name')
                data.sport =serializer_data.get('sport')
                data.age =serializer_data.get('age')
                data.save()
                return Response({"results":"sport updated "}, status=200)
            except sports.DoesNotExist:
                 return Response({"Error":"sport {} does not exist.".format(id)})
 
    def delete(self, request, id=None):
        try:
            data = sports.objects.get(id=id)
            data.delete()
            return Response({"results":"sport Deleted"}, status=200)
        except sports.DoesNotExist:
            return Response({"Error":"sport id {} does not exist.".format(id)})

