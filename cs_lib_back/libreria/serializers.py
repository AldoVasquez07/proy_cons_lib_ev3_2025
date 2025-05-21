from rest_framework import serializers
from .models import Libro, Autor, Genero, AutorLibro, LibroGenero

class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = '__all__'

class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = '__all__'

class GeneroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genero
        fields = '__all__'

class AutorLibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutorLibro
        fields = '__all__'

class LibroGeneroSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibroGenero
        fields = '__all__'
