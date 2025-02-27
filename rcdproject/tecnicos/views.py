from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Tecnico
from .serializers import TecnicoSerializer
from usuarios.permisos import RutaProtegida

class CrearTecnico(APIView):
    """
    Permite registrar un nuevo técnico.
    """
    permission_classes = [RutaProtegida(['superadmin'])]
    def post(self, request):
        serializer = TecnicoSerializer(data=request.data)
        if serializer.is_valid():
            tecnico = serializer.save()
            return Response(TecnicoSerializer(tecnico, context={'request': request}).data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListarTecnicos(APIView):
    """
    Lista todos los técnicos.
    """
    permission_classes = [RutaProtegida(['superadmin'])]
    def get(self, request):
        tecnicos = Tecnico.objects.all()
        serializer = TecnicoSerializer(tecnicos, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
