from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Transportista
from .serializers import TransportistaSerializer
from usuarios.permisos import RutaProtegida

class CrearTransportista(APIView):
    """
    Permite al coordinador (administrador) dar de alta un transportista.
    """
    permission_classes = [RutaProtegida(['superadmin', 'coordinadorlogistico'])]
    def post(self, request):
        serializer = TransportistaSerializer(data=request.data)
        if serializer.is_valid():
            transportista = serializer.save()
            # Se agrega el contexto para que el serializer pueda construir los hiperlinks correctamente.
            return Response(
                TransportistaSerializer(transportista, context={'request': request}).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListarTransportistas(APIView):
    """
    Lista todos los transportistas.
    """
    permission_classes = [RutaProtegida(['superadmin', 'coordinadorlogistico'])]
    def get(self, request):
        transportistas = Transportista.objects.all()
        serializer = TransportistaSerializer(transportistas, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class ModificarDatosTransportista(APIView):
    """
    Permite modificar los datos de un transportista
    """
    permission_classes = [RutaProtegida(['superadmin', 'coordinadorlogistico'])]
    def patch(self, request, pk):
        try:
            transportista = Transportista.objects.get(pk=pk)
        except Transportista.DoesNotExist:
            return Response({'error': 'El transportista no fue encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = TransportistaSerializer(transportista, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EliminarTransportista(APIView):
    """
    Permite eliminar un transportista
    """
    permission_classes = [RutaProtegida(['superadmin'])]
    def delete(self, request, pk):
        try:
            transportista = Transportista.objects.get(pk=pk)
        except Transportista.DoesNotExist:
            return Response({'error': 'El transportista no fue encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        
        transportista.delete()
        return Response({'mensaje': 'El transportista fue eliminado.'}, status=status.HTTP_200_OK)
