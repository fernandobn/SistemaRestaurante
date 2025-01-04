from django.db import models

# Usuario (Estudiante)
class Usuario(models.Model):
    id_estudiante = models.AutoField(primary_key=True)  # ID explícito para el Usuario
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"

# Receta
class Receta(models.Model):
    id_receta = models.AutoField(primary_key=True)  # ID explícito para la Receta
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField()
    tiempo_preparacion = models.PositiveIntegerField(help_text="Tiempo en minutos")
    dificultad = models.CharField(
        max_length=50,
        choices=[("Fácil", "Fácil"), ("Intermedio", "Intermedio"), ("Difícil", "Difícil")]
    )

    def __str__(self):
        return self.titulo


# Ingrediente
class Ingrediente(models.Model):
    id_ingrediente = models.AutoField(primary_key=True)  # ID explícito para el Ingrediente
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE, related_name="ingredientes")
    nombre = models.CharField(max_length=100)
    cantidad = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.cantidad} de {self.nombre}"

# Comentario
class Comentario(models.Model):
    id_comentario = models.AutoField(primary_key=True)  # ID explícito para el Comentario
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE, related_name="comentarios")
    estudiante = models.ForeignKey(Usuario, on_delete=models.CASCADE)  # Relación con el estudiante
    texto = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.estudiante} en {self.receta}"

