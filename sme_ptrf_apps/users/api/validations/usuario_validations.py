import logging
from django.contrib.auth import get_user_model
from rest_framework import serializers

logger = logging.getLogger(__name__)


def senhas_devem_ser_iguais(senha1, senha2):
    if senha1 != senha2:
        raise serializers.ValidationError({'detail': 'Senhas informadas devem ser iguais'})


def registro_funcional_deve_existir(registro_funcional):
    user = get_user_model()
    usuario = user.objects.filter(username=registro_funcional).exists()
    if not usuario:
        raise serializers.ValidationError({'detail': 'Registro Funcional não foi encontrado'})


def senha_nao_pode_ser_nulo(senha, campo='Senha'):
    if senha is None or senha == 'string' or len(senha) == 0:
        raise serializers.ValidationError({'detail': 'O Campo {} deve ser preenchido'.format(campo)})


def hash_redefinicao_deve_existir(hash):
    existe = get_user_model().objects.filter(hash_redefinicao=hash).exists()
    if not existe:
        logger.info("Hash não existe")
        raise serializers.ValidationError({'detail': 'Hash de redefinicação não foi encontrado'})