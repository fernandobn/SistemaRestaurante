from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Receta, Ingrediente, Usuario, Comentario
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# Vista principal
def inicio(request):
    recetas_recomendadas = Receta.objects.order_by('?')[:5]
    return render(request, 'inicio.html', {'recetas': recetas_recomendadas})


# Vista para mostrar la plantilla base (opcional)
def plantilla(request):
    return render(request, 'plantilla.html')

# Vista para crear recetas
def FormRecetas(request):
    # Obtener todas las recetas de la base de datos
    recetas = Receta.objects.all()
    
    # Renderizar el template con la lista de recetas
    return render(request, 'crearRecetas.html', {'recetas': recetas})




# Vista para mostrar las recetas y manejar la creación
def recetas(request):
    if request.method == 'POST':
        # Procesar el formulario de registro de receta
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        tiempo_preparacion = request.POST.get('tiempo_preparacion')
        dificultad = request.POST.get('dificultad')

        # Crear la receta sin asociar un usuario
        receta = Receta.objects.create(
            titulo=titulo,
            descripcion=descripcion,
            tiempo_preparacion=tiempo_preparacion,
            dificultad=dificultad
        )

        # Guardar ingredientes
        ingredientes = request.POST.getlist('ingredientes[]')
        cantidades = request.POST.getlist('cantidad[]')

        for ingrediente, cantidad in zip(ingredientes, cantidades):
            Ingrediente.objects.create(
                receta=receta,
                nombre=ingrediente,
                cantidad=cantidad
            )

        messages.success(request, "Receta guardada correctamente.")
        return redirect('recetas')  # Redirige a la misma página para actualizar el listado

    # Obtener todas las recetas para mostrar el listado
    recetas = Receta.objects.all()
    return render(request, 'crearRecetas.html', {'recetas': recetas})





def editar_receta(request, id_receta):
    try:
        receta = Receta.objects.get(id_receta=id_receta)
    except Receta.DoesNotExist:
        messages.error(request, "La receta no existe.")
        return redirect('/recetas')

    ingredientes = receta.ingredientes.all()

    return render(request, "editarRecetas.html", {
        'receta': receta,
        'ingredientes': ingredientes,
    })


def procesar_edicion_receta(request):
    if request.method == 'POST':
        try:
            receta = Receta.objects.get(id_receta=request.POST['id_receta'])
        except Receta.DoesNotExist:
            messages.error(request, "La receta no existe.")
            return redirect('/recetas')

        # Actualiza los datos de la receta
        receta.titulo = request.POST['titulo']
        receta.descripcion = request.POST['descripcion']
        receta.tiempo_preparacion = request.POST['tiempo_preparacion']
        receta.dificultad = request.POST['dificultad']
        receta.save()

        # Elimina los ingredientes existentes y agrega los nuevos
        receta.ingredientes.all().delete()
        ingredientes = request.POST.getlist('ingredientes[]')
        cantidades = request.POST.getlist('cantidad[]')

        for ingrediente, cantidad in zip(ingredientes, cantidades):
            Ingrediente.objects.create(
                receta=receta,
                nombre=ingrediente,
                cantidad=cantidad
            )

        messages.success(request, "Receta editada correctamente.")
        return redirect('/recetas')

    return redirect('/recetas')


def lista_recetas(request):
    dificultad = request.GET.get('dificultad', '')  # Obtener el valor de dificultad desde el parámetro de la URL
    if dificultad:
        # Filtrar recetas por dificultad
        recetas = Receta.objects.filter(dificultad=dificultad)
    else:
        # Si no se seleccionó ninguna dificultad, mostrar todas las recetas
        recetas = Receta.objects.all()
    
    return render(request, 'detallesReceta.html', {'recetas': recetas})


def agregar_comentario(request):
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        texto = request.POST.get('texto')
        id_receta = request.POST.get('id_receta')

        # Validar que el id_receta esté presente
        if not id_receta:
            return redirect('lista_recetas')

        # Buscar o crear el usuario
        estudiante, created = Usuario.objects.get_or_create(nombre=nombre, apellido=apellido)

        # Obtener la receta
        receta = get_object_or_404(Receta, id_receta=id_receta)

        # Crear el comentario (la fecha se asigna automáticamente)
        Comentario.objects.create(
            receta=receta,
            estudiante=estudiante,
            texto=texto
        )

        # Redirigir a la lista de recetas
        return redirect('lista_recetas')

    # En caso de método diferente a POST
    return redirect('lista_recetas')

def listado_Usuarios(request):
    # Obtener todas las recetas con sus comentarios, y sus estudiantes asociados
    recetas = Receta.objects.prefetch_related('comentarios__estudiante').all()

    # Pasar las recetas a la plantilla sin modificar los comentarios directamente
    return render(request, 'listadoUsuarios.html', {'recetas': recetas})



@csrf_exempt
def eliminar_receta(request, id_receta):
    if request.method == 'POST':
        try:
            receta = Receta.objects.get(id_receta=id_receta)
            receta.delete()
        except Receta.DoesNotExist:
            pass  # No hace nada si no existe
    return JsonResponse({})

@csrf_exempt
def eliminar_comentario(request, id_comentario):
    if request.method == 'POST':
        try:
            comentario = Comentario.objects.get(id_comentario=id_comentario)
            comentario.delete()
        except Comentario.DoesNotExist:
            pass  # No hace nada si no existe
    return JsonResponse({})

def galeria (request):
    return render(request, 'galeria.html')





