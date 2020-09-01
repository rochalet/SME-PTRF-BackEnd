from django.db.utils import IntegrityError
from rest_framework import mixins
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from ..serializers import PrestacaoContaLookUpSerializer, AtaLookUpSerializer
from ...models import PrestacaoConta, Ata
from ...services import (iniciar_prestacao_de_contas, concluir_prestacao_de_contas,
                         revisar_prestacao_de_contas, informacoes_financeiras_para_atas)


class PrestacoesContasViewSet(mixins.RetrieveModelMixin,
                              mixins.UpdateModelMixin,
                              GenericViewSet):
    permission_classes = [AllowAny]
    lookup_field = 'uuid'
    queryset = PrestacaoConta.objects.all()
    serializer_class = PrestacaoContaLookUpSerializer

    @action(detail=False, url_path='por-conta-e-periodo')
    def por_conta_e_periodo(self, request):
        conta_associacao_uuid = request.query_params.get('conta_associacao_uuid')
        periodo_uuid = request.query_params.get('periodo_uuid')
        return Response(PrestacaoContaLookUpSerializer(
            self.queryset.filter(conta_associacao__uuid=conta_associacao_uuid).filter(
                periodo__uuid=periodo_uuid).first(), many=False).data)

    @action(detail=False, methods=['post'])
    def iniciar(self, request):
        conta_associacao_uuid = request.query_params.get('conta_associacao_uuid')
        periodo_uuid = request.query_params.get('periodo_uuid')

        if not conta_associacao_uuid or not periodo_uuid:
            erro = {
                'erro': 'parametros_requerido',
                'mensagem': 'É necessário enviar o uuid do período e o uuid da conta da associação.'
            }
            return Response(erro, status=status.HTTP_400_BAD_REQUEST)

        try:
            nova_prestacao_de_contas = iniciar_prestacao_de_contas(conta_associacao_uuid, periodo_uuid)
        except(IntegrityError):
            erro = {
                'erro': 'prestacao_ja_iniciada',
                'mensagem': 'Você não pode iniciar uma prestação de contas que já foi iniciada.'
            }
            return Response(erro, status=status.HTTP_409_CONFLICT)

        return Response(PrestacaoContaLookUpSerializer(nova_prestacao_de_contas, many=False).data,
                        status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['patch'])
    def revisar(self, request, uuid):
        motivo = request.data.get('motivo', "")

        if not motivo:
            result_error = {
                'erro': 'campo_requerido',
                'mensagem': 'É necessário enviar o motivo de revisão da conciliação.'
            }
            return Response(result_error, status=status.HTTP_400_BAD_REQUEST)

        prestacao_de_conta_revista = revisar_prestacao_de_contas(prestacao_contas_uuid=uuid, motivo=motivo)
        return Response(PrestacaoContaLookUpSerializer(prestacao_de_conta_revista, many=False).data,
                        status=status.HTTP_200_OK)


    @action(detail=True, methods=['patch'])
    def concluir(self, request, uuid):
        prestacao_conta_concluida = concluir_prestacao_de_contas(prestacao_contas_uuid=uuid)
        return Response(PrestacaoContaLookUpSerializer(prestacao_conta_concluida, many=False).data,
                        status=status.HTTP_200_OK)


    @action(detail=True, methods=['get'])
    def ata(self, request, uuid):

        prestacao_conta = PrestacaoConta.by_uuid(uuid)

        ata = prestacao_conta.ultima_ata()

        if not ata:
            erro = {
                'mensagem': 'Ainda não existe uma ata para essa prestação de contas.'
            }
            return Response(erro, status=status.HTTP_404_NOT_FOUND)

        return Response(AtaLookUpSerializer(ata, many=False).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='iniciar-ata')
    def iniciar_ata(self, request, uuid):

        prestacao_conta = PrestacaoConta.by_uuid(uuid)

        ata = prestacao_conta.ultima_ata()

        if ata:
            erro = {
                'erro': 'ata-ja-iniciada',
                'mensagem': 'Já existe uma ata iniciada para essa prestação de contas.'
            }
            return Response(erro, status=status.HTTP_409_CONFLICT)

        ata = Ata.iniciar(prestacao_conta=prestacao_conta)

        return Response(AtaLookUpSerializer(ata, many=False).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='info-para-ata')
    def info_para_ata(self, request, uuid):
        prestacao_conta = self.get_object()
        result = informacoes_financeiras_para_atas(prestacao_contas=prestacao_conta)
        return Response(result, status=status.HTTP_200_OK)


    @action(detail=False, methods=['get'], url_path='fique-de-olho')
    def fique_de_olho(self, request, uuid=None):
        from sme_ptrf_apps.core.models import Parametros
        fique_de_olho = Parametros.get().fique_de_olho

        return Response({'detail': fique_de_olho}, status=status.HTTP_200_OK)
