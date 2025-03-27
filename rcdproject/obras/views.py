from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Obra, SolicitudObra, ArchivoObra
from .serializers import ObraSerializer, SolicitudObraSerializer, SolicitudObraAdminSerializer
from clientes.models import Cliente
from puntolimpio.models import PuntoLimpio
from materiales.models import Material
from usuarios.permisos import RutaProtegida
from transportistas.models import Transportista

# Importa la función de notificación para obras
from obras.notificaciones import notificar_cambio_obras

class RegistroObra(APIView):
    """
    Permite al cliente registrar una obra y los archivos adjuntos.
    """
    permission_classes = [RutaProtegida(['superadmin', 'cliente'])]

    def post(self, request):
        serializer_obra = ObraSerializer(data=request.data)
        if serializer_obra.is_valid():
            obra = serializer_obra.save()

            # Procesar y guardar los archivos enviados
            archivos = request.FILES.getlist("archivo")
            for file in archivos:
                ArchivoObra.objects.create(obra=obra, archivo=file)

            # Crear la solicitud de obra con estado "pendiente"
            solicitud = SolicitudObra.objects.create(obra=obra)
            cliente = Cliente.objects.get(pk=obra.cliente.id)
            
            # Notificar la creación (alta) de la obra vía WebSocket
            notificar_cambio_obras('alta', obra)
            
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
    permission_classes = [RutaProtegida(['superadmin', 'coordinador', 'coordinadorlogistico'])]
    
    def put(self, request, pk):
        try:
            solicitud = SolicitudObra.objects.get(pk=pk)
        except SolicitudObra.DoesNotExist:
            return Response({'error': 'Su solicitud no fue encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        
        if solicitud.estado != 'pendiente':
            return Response({'error': 'La solicitud ya ha sido procesada.'}, status=status.HTTP_400_BAD_REQUEST)
        
        solicitud.estado = 'aceptado'
        solicitud.fecha_solicitud = timezone.now()
        solicitud.save()
        
        # Notificar la aprobación de la obra (si se desea notificar en este paso)
        notificar_cambio_obras('aprobado', solicitud.obra)
        
        return Response({'mensaje': 'Su solicitud de obra fue aprobada.'}, status=status.HTTP_200_OK)


class RechazarSolicitudObra(APIView):
    """
    Permite al administrador rechazar una solicitud de obra
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
        
        # Notificar el rechazo de la obra
        notificar_cambio_obras('rechazado', solicitud.obra)
        
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
    permission_classes = [RutaProtegida(['superadmin', 'cliente', 'coordinador', 'coordinadorlogistico', 'tecnico', 'supervisor'])]
    
    def get(self, request):
        obras = Obra.objects.filter(solicitud__estado__in=['aceptado', 'terminado'])
        serializer = ObraSerializer(obras, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DetallesObra(APIView):
    """
    Muestra los detalles de una obra
    """
    permission_classes = [RutaProtegida(['superadmin', 'coordinador', 'cliente', 'tecnico', 'coordinadorlogistico'])]

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
        
        # Notificar eliminación antes de borrar
        notificar_cambio_obras('eliminado', obra)
        
        obra.delete()
        return Response({'mensaje': 'Obra eliminada.'}, status=status.HTTP_200_OK)
    

class ActualizarObra(APIView):
    """
    Permite actualizar los datos de una obra.
    """
    permission_classes = [RutaProtegida(['superadmin', 'cliente'])]

    def patch(self, request, pk):
        try:
            obra = Obra.objects.get(pk=pk)
        except Obra.DoesNotExist:
            return Response({'error': 'Obra no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ObraSerializer(obra, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            obra_actualizada = serializer.save()
            # Notificar actualización (opcional)
            notificar_cambio_obras('actualizado', obra_actualizada)
            return Response(ObraSerializer(obra_actualizada, context={'request': request}).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class MarcarObraTerminada(APIView):
    """
    Vista para marcar una obra como terminada.
    """
    permission_classes = [RutaProtegida(['superadmin', 'coordinador', 'coordinadorlogistico', 'tecnico'])]

    def put(self, request, pk):
        try:
            obra = Obra.objects.get(pk=pk)
        except Obra.DoesNotExist:
            return Response({"error": "Obra no encontrada."}, status=status.HTTP_404_NOT_FOUND)
        
        solicitud = obra.solicitud
        
        if solicitud.estado == 'terminado':
            return Response({"mensaje": "La obra ya se encuentra terminada."}, status=status.HTTP_400_BAD_REQUEST)
        
        solicitud.estado = 'terminado'
        solicitud.save()
        
        # Notificar que la obra ha sido marcada como terminada
        notificar_cambio_obras('terminado', obra)
        
        return Response({"mensaje": "Obra marcada como terminada."}, status=status.HTTP_200_OK)
    

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated 

class ListarObraPorCliente(generics.ListAPIView):
    serializer_class = ObraSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.rol == 'cliente':
            return Obra.objects.filter(cliente__usuario__email=user.email)
        return Obra.objects.none()


from supervisor_obra.serializers import SupervisorObraSerializer

class SupervisoresDeObra(APIView):
    """
    Devuelve el supervisor vinculado a la obra (o lista vacía si no hay).
    """
    permission_classes = [RutaProtegida([
        'superadmin', 
        'coordinador', 
        'coordinadorlogistico',
        'tecnico',
        'supervisor',
        'cliente'
    ])]

    def get(self, request, pk):
        try:
            obra = Obra.objects.get(pk=pk)
        except Obra.DoesNotExist:
            return Response({"error": "Obra no encontrada."}, status=status.HTTP_404_NOT_FOUND)
        
        if not hasattr(obra, 'supervisor'):
            return Response([], status=status.HTTP_200_OK)
        
        sup = obra.supervisor  
        serializer = SupervisorObraSerializer(sup) 
        return Response([serializer.data], status=status.HTTP_200_OK)
