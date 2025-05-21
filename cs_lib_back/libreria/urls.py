from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LibroViewSet, AutorViewSet, GeneroViewSet, AutorLibroViewSet, LibroGeneroViewSet


router = DefaultRouter()
router.register(r'libros', LibroViewSet)
router.register(r'autores', AutorViewSet)
router.register(r'generos', GeneroViewSet)
router.register(r'autor-libro', AutorLibroViewSet)
router.register(r'libro-genero', LibroGeneroViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
