from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from sme_ptrf_apps.core.models import AcaoAssociacao, ContaAssociacao, DemonstrativoFinanceiro, Periodo
from sme_ptrf_apps.core.services.demonstrativo_financeiro import gerar
from sme_ptrf_apps.core.services.info_por_acao_services import info_acoes_associacao_no_periodo


class DemonstrativoFinanceiroViewSet(GenericViewSet):
    permission_classes = [AllowAny]
    lookup_field = 'uuid'
    queryset = DemonstrativoFinanceiro.objects.all()

    @action(detail=False, methods=['get'])
    def previa(self, request):
        response = self._gerar_planilha(request)
        return response

    @action(detail=False, methods=['get'], url_path='documento-final')
    def documento_final(self, request):
        acao_associacao_uuid = self.request.query_params.get('acao-associacao')
        acao_associacao = AcaoAssociacao.objects.filter(uuid=acao_associacao_uuid).get()
        DemonstrativoFinanceiro.objects.update_or_create(acao_associacao=acao_associacao)
        response = self._gerar_planilha(request)
        return response

    @action(detail=False, methods=['get'])
    def acoes(self, request):
        periodo = None

        associacao_uuid = request.query_params.get('associacao_uuid') 
        periodo_uuid = request.query_params.get('periodo_uuid')

        if not associacao_uuid or not periodo_uuid:
            erro = {
                'erro': 'parametros_requeridos',
                'mensagem': 'É necessário enviar o uuid do período e o uuid da associação.'
            }
            return Response(erro, status=status.HTTP_400_BAD_REQUEST)

        if periodo_uuid:
            periodo = Periodo.by_uuid(periodo_uuid)

        if not periodo:
            periodo = Periodo.periodo_atual()

        info_acoes = info_acoes_associacao_no_periodo(associacao_uuid=associacao_uuid, periodo=periodo)
        result = {
            'info_acoes': info_acoes
        }

        return Response(result)
    
    @action(detail=False, methods=['get'], url_path='demonstrativo-info')
    def demonstrativo_info(self, request):
        acao_associacao_uuid = self.request.query_params.get('acao-associacao')
        demonstrativo_financeiro = DemonstrativoFinanceiro.objects.filter(acao_associacao__uuid=acao_associacao_uuid).last()
        msg = str(demonstrativo_financeiro) if demonstrativo_financeiro else 'Documento pendente de geração'
        return Response(msg)

    def _gerar_planilha(self, request):
        acao_associacao_uuid = self.request.query_params.get('acao-associacao')
        conta_associacao_uuid = self.request.query_params.get('conta-associacao')
        periodo_uuid = self.request.query_params.get('periodo')

        if not acao_associacao_uuid or not conta_associacao_uuid or not periodo_uuid:
            erro = {
                'erro': 'parametros_requeridos',
                'mensagem': 'É necessário enviar o uuid do período, o uuid da ação da associação e o uuid da conta da associação.'
            }
            return Response(erro, status=status.HTTP_400_BAD_REQUEST)

        acao_associacao = AcaoAssociacao.objects.filter(uuid=acao_associacao_uuid).get()
        conta_associacao = ContaAssociacao.objects.filter(uuid=conta_associacao_uuid).get()
        periodo = Periodo.objects.filter(uuid=periodo_uuid).get()

        stream = gerar(periodo, acao_associacao, conta_associacao)

        from django.http import HttpResponse
        
        filename = 'demonstrativo_financeiro.xlsx'
        response = HttpResponse(
            stream,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        
        return response