# progress/views.py

from rest_framework import generics
from .models import Progress
from .serializers import ProgressSerializer

class ProgressView(generics.RetrieveUpdateAPIView):
    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer
