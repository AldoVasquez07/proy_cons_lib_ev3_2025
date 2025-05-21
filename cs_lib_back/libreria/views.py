from rest_framework import viewsets
from .models import Libro, Autor, Genero, AutorLibro, LibroGenero
from .serializers import LibroSerializer, AutorSerializer, GeneroSerializer, AutorLibroSerializer, LibroGeneroSerializer

class LibroViewSet(viewsets.ModelViewSet):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer

class AutorViewSet(viewsets.ModelViewSet):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer

class GeneroViewSet(viewsets.ModelViewSet):
    queryset = Genero.objects.all()
    serializer_class = GeneroSerializer

class AutorLibroViewSet(viewsets.ModelViewSet):
    queryset = AutorLibro.objects.all()
    serializer_class = AutorLibroSerializer

class LibroGeneroViewSet(viewsets.ModelViewSet):
    queryset = LibroGenero.objects.all()
    serializer_class = LibroGeneroSerializer
