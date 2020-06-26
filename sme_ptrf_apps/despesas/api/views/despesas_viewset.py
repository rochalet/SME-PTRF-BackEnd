from rest_framework import mixins
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from ..serializers.despesa_serializer import DespesaSerializer, DespesaCreateSerializer
from ..serializers.tipo_custeio_serializer import TipoCusteioSerializer
from ..serializers.tipo_documento_serializer import TipoDocumentoSerializer
from ..serializers.tipo_transacao_serializer import TipoTransacaoSerializer
from ...models import Despesa
from ...tipos_aplicacao_recurso import aplicacoes_recurso_to_json
from ....core.api.serializers.acao_associacao_serializer import AcaoAssociacaoLookUpSerializer
from ....core.api.serializers.conta_associacao_serializer import ContaAssociacaoLookUpSerializer


class DespesasViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      GenericViewSet):
    permission_classes = [AllowAny]
    lookup_field = 'uuid'
    queryset = Despesa.objects.all()
    serializer_class = DespesaSerializer

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return DespesaSerializer
        else:
            return DespesaCreateSerializer

    @action(detail=False, url_path='tabelas')
    def tabelas(self, request):

        def get_valores_from(serializer):
            valores = serializer.Meta.model.get_valores(user=request.user)
            return serializer(valores, many=True).data if valores else []

        result = {
            'tipos_aplicacao_recurso': aplicacoes_recurso_to_json(),
            'tipos_custeio': get_valores_from(TipoCusteioSerializer),
            'tipos_documento': get_valores_from(TipoDocumentoSerializer),
            'tipos_transacao': get_valores_from(TipoTransacaoSerializer),
            'acoes_associacao': get_valores_from(AcaoAssociacaoLookUpSerializer),
            'contas_associacao': get_valores_from(ContaAssociacaoLookUpSerializer)
        }

        return Response(result)

    @action(detail=False, url_path='ja-lancada')
    def ja_lancada(self, request):

        tipo_documento = request.query_params.get('tipo_documento')

        if tipo_documento is None:
            erro = {
                'erro': 'parametros_requerido',
                'mensagem': 'É necessário enviar a o id do tipo de documento como parâmetro. Ex: tipo_documento=1.'
            }
            return Response(erro, status=status.HTTP_400_BAD_REQUEST)

        numero_documento = request.query_params.get('numero_documento')
        if numero_documento is None:
            erro = {
                'erro': 'parametros_requerido',
                'mensagem': 'É necessário enviar a o número do documento como parâmetro. Ex: numero_documento=123.'
            }
            return Response(erro, status=status.HTTP_400_BAD_REQUEST)

        cpf_cnpj_fornecedor = request.query_params.get('cpf_cnpj_fornecedor')
        if cpf_cnpj_fornecedor is None:
            erro = {
                'erro': 'parametros_requerido',
                'mensagem': 'É necessário enviar a o número do documento como parâmetro. Ex: cpf_cnpj_fornecedor=455..'
            }
            return Response(erro, status=status.HTTP_400_BAD_REQUEST)

        associacao__uuid = request.query_params.get('associacao__uuid')
        if associacao__uuid is None:
            erro = {
                'erro': 'parametros_requerido',
                'mensagem': 'É necessário enviar a o uuid da associação como parâmetro. Ex: associacao__uuid=GSDHH3434..'
            }
            return Response(erro, status=status.HTTP_400_BAD_REQUEST)

        despesa_uuid = request.query_params.get('despesa_uuid')

        despesa = Despesa.by_documento(tipo_documento=tipo_documento, numero_documento=numero_documento,
                                       cpf_cnpj_fornecedor=cpf_cnpj_fornecedor, associacao__uuid=associacao__uuid)

        despesa_ja_lancada = despesa is not None and f'{despesa.uuid}' != despesa_uuid

        result = {
            'despesa_ja_lancada': despesa_ja_lancada,
            'uuid_despesa': f'{despesa.uuid}' if despesa_ja_lancada else ''
        }

        return Response(result)
