from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Obra, SolicitudObra
from .serializers import ObraSerializer, SolicitudObraSerializer, SolicitudObraAdminSerializer
from clientes.models import Cliente
from puntolimpio.models import PuntoLimpio
from materiales.models import Material
from usuarios.permisos import RutaProtegida
from transportistas.models import Transportista

class RegistroObra(APIView):
    """
    Permite al cliente registrar una obra, creando automáticamente la solicitud 
    con estado "pendiente". Los puntos limpios y los materiales se registrarán
    por separado.
    """
    permission_classes = [RutaProtegida(['superadmin', 'cliente'])]
    def post(self, request):
        serializer_obra = ObraSerializer(data=request.data)
        if serializer_obra.is_valid():
            obra = serializer_obra.save()
            # Crear la solicitud de obra con estado "pendiente"
            solicitud = SolicitudObra.objects.create(obra=obra)
            cliente = Cliente.objects.get(pk=obra.cliente.id)
            
            return Response({
                'mensaje': 'Obra registrada, pendiente de aprobación.',
                'obra': ObraSerializer(obra, context={'request': request}).data,
                'solicitud': SolicitudObraSerializer(solicitud, context={'request': request}).data,
                'ID de cliente': cliente.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer_obra.errors, status=status.HTTP_400_BAD_REQUEST)


class ListarSolicitudesObra(APIView):
    """
    Lista todas las solicitudes de obras para el administrador
    """
    permission_classes = [RutaProtegida(['superadmin', 'coordinador', 'coordinadorlogistico'])]
    def get(self, request):
        solicitudes = SolicitudObra.objects.all()
        serializer = SolicitudObraAdminSerializer(solicitudes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AprobarSolicitudObra(APIView):
    """
    Permite al administrador aceptar una solicitud de obra
    """
    permission_classes = [RutaProtegida(['superadmin'])]
    def put(self, request, pk):
        try:
            solicitud = SolicitudObra.objects.get(pk=pk)
        except SolicitudObra.DoesNotExist:
            return Response({'error': 'Su solicitud no fue encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        
        if solicitud.estado != 'pendiente':
            return Response({'error': 'La solicitud ya ha sido procesada.'}, status=status.HTTP_400_BAD_REQUEST)
        
        solicitud.estado = 'Aceptado'
        solicitud.fecha_solicitud = timezone.now()
        solicitud.save()
        return Response({'mensaje': 'Su solicitud de obra fue aprobada.'}, status=status.HTTP_200_OK)

class RechazarSolicitudObra(APIView):
    """
    Permite al administrador rechazar una solicitud de obra.
    Al rechazar, se eliminan los puntos limpios y los materiales asociados a la obra.
    """
    permission_classes = [RutaProtegida(['superadmin'])]
    def put(self, request, pk):
        try:
            solicitud = SolicitudObra.objects.get(pk=pk)
        except SolicitudObra.DoesNotExist:
            return Response({'error': 'Su solicitud no fue encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        
        if solicitud.estado != 'pendiente':
            return Response({'error': 'La solicitud ya ha sido procesada.'}, status=status.HTTP_400_BAD_REQUEST)
        
        solicitud.estado = 'rechazado'
        solicitud.save()
        
        obra = solicitud.obra
        obra.puntos_limpios.all().delete()
        obra.materiales.all().delete()
        
        return Response(
            {'mensaje': 'Su solicitud de obra fue rechazada y se eliminaron los puntos limpios y materiales asociados.'},
            status=status.HTTP_200_OK
        )

class ListarObrasAprobadas(APIView):
    """
    Muestra una lista con las obras que fueron aprobadas
    """
    permission_classes = [RutaProtegida(['superadmin', 'cliente', 'coordinador', 'coordinadorlogistico'])]
    def get(self, request):
        obras = Obra.objects.filter(solicitud__estado='Aceptado')
        serializer = ObraSerializer(obras, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ModificarDatosObra(APIView):
    """
    Modificar datos de obras
    """
    permission_classes = [RutaProtegida(['superadmin', 'cliente'])]
    def patch(self, request, pk):
        try:
            obra = Obra.objects.get(pk=pk)
        except Obra.DoesNotExist:
            return Response({'error': 'Obra no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ObraSerializer(obra, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DetallesObra(APIView):
    """
    Muestra los detalles de una obra
    """
    permission_classes = [RutaProtegida(['superadmin', 'coordinador'])]

    def get(self, request, pk):
        try:
            obra = Obra.objects.get(pk=pk)
        except Obra.DoesNotExist:
            return Response({'error': 'Obra no encontrada.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ObraSerializer(obra, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class EliminarObra(APIView):
    """
    Eliminar una obra
    """
    permission_classes = [RutaProtegida(['superadmin', 'cliente'])]
    def delete(self, request, pk):
        try:
            obra = Obra.objects.get(pk=pk)
        except Obra.DoesNotExist:
            return Response({'error': 'Obra no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        
        obra.delete()
        return Response({'mensaje': 'Obra eliminada.'}, status=status.HTTP_200_OK)
    