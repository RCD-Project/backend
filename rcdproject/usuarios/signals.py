from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from clientes.models import Cliente

Usuario = get_user_model()

@receiver(post_save, sender=Usuario)
def crear_token_automatico(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

@receiver(post_save, sender=Cliente)
def crear_usuario_asociado(sender, instance, created, **kwargs):
    if created:
        Usuario.objects.create_user(
            username=instance.mail,
            email=instance.mail,
            password="PasswordPorDefectoOGenerado",  
            first_name=instance.nombre,  
            rol='cliente'
        )
