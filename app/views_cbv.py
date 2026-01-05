from rest_framework import generics
from .models import Car
from .serializers import CarSerializer


#CBV
class CarListCreateView(generics.ListCreateAPIView):
    queryset = Car.objects.all().order_by("-id")
    serializer_class = CarSerializer


class CarDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer