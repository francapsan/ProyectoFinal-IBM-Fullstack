from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime

class CarMake(models.Model):
    """
    Modelo para gestionar las marcas de automóviles (Car Makes)
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la Marca")
    description = models.TextField(blank=True, verbose_name="Descripción")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")

    class Meta:
        verbose_name = "Marca de Coche"
        verbose_name_plural = "Marcas de Coches"
        ordering = ['name']

    def __str__(self):
        return self.name


class CarModel(models.Model):
    """
    Modelo para gestionar los modelos de automóviles asociados a una marca (Car Models)
    """
    CAR_TYPES = [
        ('SEDAN', 'Sedán'),
        ('SUV', 'SUV / Todoterreno'),
        ('WAGON', 'Familiar / Wagon'),
        ('COUPE', 'Coupé Deportivo'),
        ('HATCHBACK', 'Compacto / Hatchback'),
        ('PICKUP', 'Camioneta Pickup'),
        ('CONVERTIBLE', 'Descapotable / Convertible')
    ]

    current_year = datetime.date.today().year

    make = models.ForeignKey(
        CarMake, 
        on_delete=models.CASCADE, 
        related_name='models',
        verbose_name="Marca de Coche"
    )
    name = models.CharField(max_length=100, verbose_name="Nombre del Modelo")
    dealer_id = models.IntegerField(default=1, verbose_name="ID de Concesionario Asignado")
    type = models.CharField(
        max_length=20, 
        choices=CAR_TYPES, 
        default='SEDAN',
        verbose_name="Tipo de Vehículo"
    )
    year = models.IntegerField(
        default=current_year,
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(current_year + 1)
        ],
        verbose_name="Año de Fabricación"
    )

    class Meta:
        verbose_name = "Modelo de Coche"
        verbose_name_plural = "Modelos de Coches"
        ordering = ['make', 'name', '-year']

    def __str__(self):
        return f"{self.make.name} {self.name} ({self.year}) - {self.get_type_display()}"
