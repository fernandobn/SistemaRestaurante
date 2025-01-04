from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('plantilla/', views.plantilla, name='plantilla'),
    path('FormRecetas/', views.FormRecetas, name='FormRecetas'),
    path('recetas/', views.recetas, name='recetas'),
    path('editar_receta/<int:id_receta>/', views.editar_receta, name='editar_receta'),
    path('procesar_edicion_receta/', views.procesar_edicion_receta),
    path('lista_recetas/', views.lista_recetas, name='lista_recetas'),
    path('agregar_comentario/', views.agregar_comentario, name='agregar_comentario'),
    path('listado_Usuarios/', views.listado_Usuarios, name='listado_Usuarios'),
    path('eliminarReceta/<int:id_receta>/', views.eliminar_receta, name='eliminar_receta'),
    path('eliminarComentario/<int:id_comentario>/', views.eliminar_comentario, name='eliminar_comentario'),
    path('galeria/', views.galeria, name='galeria'),

]





