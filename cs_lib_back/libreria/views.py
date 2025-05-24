from rest_framework import viewsets
from .models import Libro, Autor, Genero, AutorLibro, LibroGenero
from .serializers import LibroSerializer, AutorSerializer, GeneroSerializer, AutorLibroSerializer, LibroGeneroSerializer
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework import status

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

    def get_queryset(self):
        queryset = super().get_queryset()
        autor_id = self.request.query_params.get('autor')
        libro_id = self.request.query_params.get('libro')

        if autor_id is not None:
            queryset = queryset.filter(autor_id=autor_id)

        if libro_id is not None:
            queryset = queryset.filter(libro_id=libro_id)

        return queryset



class LibroGeneroViewSet(viewsets.ModelViewSet):
    queryset = LibroGenero.objects.all()
    serializer_class = LibroGeneroSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        libro_id = self.request.query_params.get('libro')
        genero_id = self.request.query_params.get('genero')

        if libro_id is not None:
            queryset = queryset.filter(libro_id=libro_id)

        if genero_id is not None:
            queryset = queryset.filter(genero_id=genero_id)

        return queryset
