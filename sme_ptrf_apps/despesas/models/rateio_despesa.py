from decimal import Decimal

from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from sme_ptrf_apps.core.models_abstracts import ModeloBase
from ..status_cadastro_completo import STATUS_CHOICES, STATUS_COMPLETO, STATUS_INCOMPLETO
from ..tipos_aplicacao_recurso import APLICACAO_CHOICES, APLICACAO_CUSTEIO, APLICACAO_CAPITAL


class RateioDespesa(ModeloBase):
    despesa = models.ForeignKey('Despesa', on_delete=models.CASCADE, related_name='rateios', blank=True, null=True)

    associacao = models.ForeignKey('core.Associacao', on_delete=models.PROTECT, related_name='rateios_associacao',
                                   blank=True, null=True)

    conta_associacao = models.ForeignKey('core.ContaAssociacao', on_delete=models.PROTECT,
                                         related_name='rateios_da_conta', blank=True, null=True)

    acao_associacao = models.ForeignKey('core.AcaoAssociacao', on_delete=models.PROTECT,
                                        related_name='rateios_da_associacao', blank=True, null=True)

    aplicacao_recurso = models.CharField(
        'Tipo de aplicação do recurso',
        max_length=15,
        choices=APLICACAO_CHOICES,
        default=APLICACAO_CUSTEIO,
        null=True,
    )

    tipo_custeio = models.ForeignKey('TipoCusteio', on_delete=models.PROTECT, blank=True, null=True)

    especificacao_material_servico = models.ForeignKey('EspecificacaoMaterialServico', on_delete=models.PROTECT,
                                                       blank=True, null=True)

    valor_rateio = models.DecimalField('Valor', max_digits=8, decimal_places=2, default=0)

    quantidade_itens_capital = models.PositiveSmallIntegerField('Quantidade de itens', default=0)
    valor_item_capital = models.DecimalField('Valor unitário ', max_digits=8, decimal_places=2, default=0)
    numero_processo_incorporacao_capital = models.CharField('Nº processo incorporação', max_length=100, default='',
                                                            blank=True)

    status = models.CharField(
        'status',
        max_length=15,
        choices=STATUS_CHOICES,
        default=STATUS_INCOMPLETO
    )

    conferido = models.BooleanField('Conferido?', default=False)

    prestacao_conta = models.ForeignKey('core.PrestacaoConta', on_delete=models.SET_NULL, blank=True, null=True,
                                        related_name='despesas_conciliadas',
                                        verbose_name='prestação de contas de conciliação')

    def __str__(self):
        documento = self.despesa.numero_documento if self.despesa else 'Despesa indefinida'
        return f"{documento} - {self.valor_rateio:.2f}"

    def cadastro_completo(self):
        completo = self.conta_associacao and \
                   self.acao_associacao and \
                   self.aplicacao_recurso and \
                   self.especificacao_material_servico and \
                   self.valor_rateio

        if self.aplicacao_recurso == APLICACAO_CUSTEIO:
            completo = completo and self.tipo_custeio

        if self.aplicacao_recurso == APLICACAO_CAPITAL:
            completo = completo and \
                       self.quantidade_itens_capital > 0 and \
                       self.valor_item_capital > 0 and self.numero_processo_incorporacao_capital

        return completo

    @classmethod
    def rateios_da_acao_associacao_no_periodo(cls, acao_associacao, periodo, conferido=None, conta_associacao=None,
                                              exclude_despesa=None, aplicacao_recurso=None):
        if periodo.data_fim_realizacao_despesas:
            dataset = cls.objects.filter(acao_associacao=acao_associacao).filter(
                despesa__data_documento__range=(
                    periodo.data_inicio_realizacao_despesas, periodo.data_fim_realizacao_despesas))
        else:
            dataset = cls.objects.filter(acao_associacao=acao_associacao).filter(
                despesa__data_documento__gte=periodo.data_inicio_realizacao_despesas)

        if conferido is not None:
            dataset = dataset.filter(conferido=conferido)

        if conta_associacao:
            dataset = dataset.filter(conta_associacao=conta_associacao)

        if exclude_despesa:
            dataset = dataset.exclude(despesa__uuid=exclude_despesa)

        if aplicacao_recurso:
            dataset = dataset.filter(aplicacao_recurso=aplicacao_recurso)

        return dataset.all()

    @classmethod
    def rateios_da_conta_associacao_no_periodo(cls, conta_associacao, periodo, conferido=None,
                                               exclude_despesa=None, aplicacao_recurso=None):
        if periodo.data_fim_realizacao_despesas:
            dataset = cls.objects.filter(conta_associacao=conta_associacao).filter(
                despesa__data_documento__range=(
                    periodo.data_inicio_realizacao_despesas, periodo.data_fim_realizacao_despesas))
        else:
            dataset = cls.objects.filter(acao_associacao=conta_associacao).filter(
                despesa__data_documento__gte=periodo.data_inicio_realizacao_despesas)

        if conferido is not None:
            dataset = dataset.filter(conferido=conferido)

        if exclude_despesa:
            dataset = dataset.exclude(despesa__uuid=exclude_despesa)

        if aplicacao_recurso:
            dataset = dataset.filter(aplicacao_recurso=aplicacao_recurso)

        return dataset.all()

    @classmethod
    def especificacoes_dos_rateios_da_acao_associacao_no_periodo(cls, acao_associacao, periodo, conferido=None,
                                                                 conta_associacao=None,
                                                                 exclude_despesa=None):

        rateios = cls.rateios_da_acao_associacao_no_periodo(acao_associacao=acao_associacao,
                                                            periodo=periodo, conferido=conferido,
                                                            conta_associacao=conta_associacao,
                                                            exclude_despesa=exclude_despesa)

        especificacoes = {
            APLICACAO_CAPITAL: set(),
            APLICACAO_CUSTEIO: set()
        }
        for rateio in rateios:
            if rateio.especificacao_material_servico:
                especificacoes[rateio.aplicacao_recurso].add(rateio.especificacao_material_servico.descricao)

        return {
            APLICACAO_CAPITAL: sorted(especificacoes[APLICACAO_CAPITAL]),
            APLICACAO_CUSTEIO: sorted(especificacoes[APLICACAO_CUSTEIO])
        }

    def marcar_conferido(self, prestacao_conta=None):
        self.conferido = True
        self.prestacao_conta = prestacao_conta
        self.save()
        return self

    def desmarcar_conferido(self):
        self.conferido = False
        self.prestacao_conta = None
        self.save()
        return self

    @classmethod
    def conciliar(cls, uuid, prestacao_conta):
        rateio_despesa = cls.by_uuid(uuid)
        return rateio_despesa.marcar_conferido(prestacao_conta)

    @classmethod
    def desconciliar(cls, uuid):
        rateio_despesa = cls.by_uuid(uuid)
        return rateio_despesa.desmarcar_conferido()

    @classmethod
    def totais_por_acao_associacao_no_periodo(cls, acao_associacao, periodo):
        despesas = cls.rateios_da_acao_associacao_no_periodo(acao_associacao=acao_associacao,
                                                             periodo=periodo)
        totais = {
            'total_despesas_capital': Decimal(0.00),
            'total_despesas_custeio': Decimal(0.00),
            'total_despesas_nao_conciliadas_capital': Decimal(0.00),
            'total_despesas_nao_conciliadas_custeio': Decimal(0.00),
        }

        for despesa in despesas:
            if despesa.aplicacao_recurso == APLICACAO_CAPITAL:
                totais['total_despesas_capital'] += despesa.valor_rateio
            else:
                totais['total_despesas_custeio'] += despesa.valor_rateio

            if not despesa.conferido:
                if despesa.aplicacao_recurso == APLICACAO_CAPITAL:
                    totais['total_despesas_nao_conciliadas_capital'] += despesa.valor_rateio
                else:
                    totais['total_despesas_nao_conciliadas_custeio'] += despesa.valor_rateio

        return totais

    class Meta:
        verbose_name = "Rateio de despesa"
        verbose_name_plural = "Rateios de despesas"


@receiver(pre_save, sender=RateioDespesa)
def rateio_pre_save(instance, **kwargs):
    instance.status = STATUS_COMPLETO if instance.cadastro_completo() else STATUS_INCOMPLETO


@receiver(post_save, sender=RateioDespesa)
def rateio_post_save(instance, created, **kwargs):
    if instance and instance.despesa:
        instance.despesa.atualiza_status()
