from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework import generics

from .models import Car
from .serializers import CarSerializer


#FBV

@api_view(['POST', 'GET'])
def car_list_create(request):
    if request.method == "GET":
        cars = Car.objects.all().order_by("-id")
        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data)
    

    #POST
    serializer = CarSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(["PUT", "PATCH", "DELETE", "GET"])
def car_detail_update_delete(request, pk:int):
    car = get_object_or_404(Car, pk=pk)

    if request.method == "GET":
        serializer = CarSerializer(car)
        return Response(serializer.data)
    

    if request.method in ["PUT", "PATCH"]:
        partial = (request.method == "PATCH")
        serializer = CarSerializer(car, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE
    car.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)



