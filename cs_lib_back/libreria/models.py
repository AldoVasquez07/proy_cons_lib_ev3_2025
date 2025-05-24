from django.db import models
from django.utils import timezone

class Libro(models.Model):
    codigo = models.CharField(max_length=150, unique=True)
    nombre = models.CharField(max_length=150)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    flag = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Autor(models.Model):
    dni = models.CharField(max_length=8, unique=True)
    codigo = models.CharField(max_length=8, unique=True)
    nombre = models.CharField(max_length=150)
    apellido_paterno = models.CharField(max_length=150)
    apellido_materno = models.CharField(max_length=150)
    fecha_nacimiento = models.DateTimeField(default=timezone.now)
    flag = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.nombre} {self.apellido_paterno} {self.apellido_materno}'


class Genero(models.Model):
    codigo = models.CharField(max_length=8, unique=True)
    nombre = models.CharField(max_length=150)
    flag = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class AutorLibro(models.Model):
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name='autor_libros')
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='libro_autores')
    flag = models.BooleanField(default=True)

    class Meta:
        unique_together = ('autor', 'libro')

    def __str__(self):
        return f'{self.autor} - {self.libro}'


class LibroGenero(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='libro_generos')
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE, related_name='genero_libros')
    flag = models.BooleanField(default=True)

    class Meta:
        unique_together = ('libro', 'genero')

    def __str__(self):
        return f'{self.libro} - {self.genero}'
