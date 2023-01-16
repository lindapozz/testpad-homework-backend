from django.shortcuts import render
from rest_framework import viewsets
from .serializers import UrlSerializer
from .models import Url

# Create your views here.
class UrlView(viewsets.ModelViewSet):
    serializer_class = UrlSerializer
    queryset = Url.objects.all()