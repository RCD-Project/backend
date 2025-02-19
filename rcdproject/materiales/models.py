from django.db import models
from django.db import models
from puntolimpio.models import PuntoLimpio
from obras.models import Obra  
from transportistas.models import Transportista 
from django.core.exceptions import ValidationError

class Material(models.Model):
    id = models.AutoField(primary_key=True)
    TIPO_MATERIAL_CHOICES = [
        ('escombro_limpio', 'Escombro Limpio'),
        ('plastico', 'Plástico'),
        ('papel_carton', 'Papel y Cartón'),
        ('metales', 'Metales'),
        ('madera', 'Madera'),
        ('mezclados', 'Mezclados'),
        ('peligrosos', 'Peligrosos'),
    ]
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE, related_name='materiales', verbose_name="Obra")
    punto_limpio = models.ForeignKey(PuntoLimpio, on_delete=models.CASCADE, related_name='materiales', verbose_name="Punto Limpio")
    transportista = models.ForeignKey(Transportista, on_delete=models.CASCADE, related_name='materiales', verbose_name="Transportista")
    descripcion = models.TextField("Descripción")
    proteccion = models.CharField("Protección", max_length=200)
    tipo_contenedor = models.CharField("Tipo de Contenedor", max_length=200)
    estado_del_contenedor = models.CharField("Estado del Contenedor", max_length=200)
    esta_lleno = models.BooleanField("Está lleno", default=False)
    tipo_material = models.CharField("Tipo de Material", max_length=20, choices=TIPO_MATERIAL_CHOICES)
    ventilacion = models.CharField("Ventilación", max_length=100, null=True, blank=True, help_text="Obligatorio si el material es 'peligrosos'")

    def clean(self):
        if self.tipo_material == 'peligrosos':
            if not self.ventilacion or self.ventilacion.strip() == "":
                raise ValidationError("Para materiales peligrosos, el campo 'Ventilación' es obligatorio.")
        else:
            if self.ventilacion and self.ventilacion.strip() != "":
                raise ValidationError("El campo 'Ventilación' debe estar vacío cuando el material no es 'peligrosos'.")
        
        if self.transportista and self.transportista.tipo_material != self.tipo_material:
            raise ValidationError("El transportista seleccionado no puede transportar este tipo de material.")



    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)