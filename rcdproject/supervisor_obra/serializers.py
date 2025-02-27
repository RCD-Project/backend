from .models import SupervisorObra
from rest_framework import serializers

class SupervisorObraSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupervisorObra
        fields = ['id', 'nombre', 'telefono', 'email', 'obra', 'nivel_capacitacion']
        read_only_fields = ['id']
        