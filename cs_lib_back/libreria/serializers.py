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
    # Campos para mostrar detalles (solo lectura)
    autor_detalle = serializers.SerializerMethodField(read_only=True)
    libro_detalle = serializers.SerializerMethodField(read_only=True)

    # Campos para recibir IDs al crear/actualizar
    autor = serializers.PrimaryKeyRelatedField(queryset=Autor.objects.all())
    libro = serializers.PrimaryKeyRelatedField(queryset=Libro.objects.all())

    class Meta:
        model = AutorLibro
        fields = ['id', 'autor', 'libro', 'flag', 'autor_detalle', 'libro_detalle']

    def get_autor_detalle(self, obj):
        return {
            'id': obj.autor.id,
            'nombre': obj.autor.nombre,
            'apellido_paterno': obj.autor.apellido_paterno,
            'apellido_materno': obj.autor.apellido_materno
        }

    def get_libro_detalle(self, obj):
        return {
            'id': obj.libro.id,
            'codigo': obj.libro.codigo,
            'nombre': obj.libro.nombre
        }

    def validate(self, data):
        autor = data.get('autor')
        libro = data.get('libro')
        print(f"Validando relación autor={autor}, libro={libro}")

        existe = AutorLibro.objects.filter(autor=autor, libro=libro).exists()
        print(f"Existe relación?: {existe}")

        if existe:
            raise serializers.ValidationError("La relación entre este autor y libro ya existe.")
        return data


class LibroGeneroSerializer(serializers.ModelSerializer):
    # Campos para mostrar detalles (solo lectura)
    libro_detalle = serializers.SerializerMethodField(read_only=True)
    genero_detalle = serializers.SerializerMethodField(read_only=True)

    # Campos para recibir IDs al crear/actualizar
    libro = serializers.PrimaryKeyRelatedField(queryset=Libro.objects.all())
    genero = serializers.PrimaryKeyRelatedField(queryset=Genero.objects.all())

    class Meta:
        model = LibroGenero
        fields = ['id', 'libro', 'genero', 'flag', 'libro_detalle', 'genero_detalle']
        

    def get_libro_detalle(self, obj):
        return {
            'id': obj.libro.id,
            'codigo': obj.libro.codigo,
            'nombre': obj.libro.nombre
        }

    def get_genero_detalle(self, obj):
        return {
            'id': obj.genero.id,
            'codigo': obj.genero.codigo,
            'nombre': obj.genero.nombre
        }

    def validate(self, data):
        libro = data.get('libro')
        genero = data.get('genero')
        existe = LibroGenero.objects.filter(libro=libro, genero=genero).exists()
        if existe:
            raise serializers.ValidationError("La relación entre este libro y género ya existe.")
        return data

