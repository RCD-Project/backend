from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Material
from .serializers import MaterialSerializer
from django.core.exceptions import ValidationError as DjangoValidationError

class CrearMaterial(APIView):
    """
    Permite crear un nuevo Material asociado a un Punto Limpio y un Transportista.
    """
    def post(self, request):
        serializer = MaterialSerializer(data=request.data)
        if serializer.is_valid():
            try:
                material = serializer.save()
            except DjangoValidationError as e:
                return Response(e.message_dict, status=status.HTTP_400_BAD_REQUEST)
            return Response(MaterialSerializer(material, context={'request': request}).data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListarMateriales(APIView):
    """
    Lista todos los materiales.
    """
    def get(self, request):
        materiales = Material.objects.all()
        serializer = MaterialSerializer(materiales, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

