from enum import Enum

from django.db import models

from sme_ptrf_apps.core.models import Associacao, Periodo
from sme_ptrf_apps.core.models_abstracts import ModeloBase

from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog


class StatusRepasse(Enum):
    PENDENTE = 'Pendente'
    REALIZADO = 'Realizado'

STATUS_CHOICES = (
    (StatusRepasse.PENDENTE.name, StatusRepasse.PENDENTE.value),
    (StatusRepasse.REALIZADO.name, StatusRepasse.REALIZADO.value),
)


class Repasse(ModeloBase):
    history = AuditlogHistoryField()
    associacao = models.ForeignKey(Associacao, on_delete=models.PROTECT, related_name='repasses',
                                   blank=True, null=True)

    valor_capital = models.DecimalField('Valor Capital', max_digits=20, decimal_places=2, default=0)

    valor_custeio = models.DecimalField('Valor Custeio', max_digits=20, decimal_places=2, default=0)

    valor_livre = models.DecimalField('Valor Livre Aplicação', max_digits=20, decimal_places=2, default=0)

    conta_associacao = models.ForeignKey('core.ContaAssociacao', on_delete=models.PROTECT,
                                         related_name='repasses_da_conta', blank=True, null=True)

    acao_associacao = models.ForeignKey('core.AcaoAssociacao', on_delete=models.PROTECT,
                                        related_name='repasses_da_associacao', blank=True, null=True)

    periodo = models.ForeignKey(Periodo, on_delete=models.PROTECT,
                                related_name='+', blank=True, null=True)

    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default=StatusRepasse.PENDENTE.value
    )

    realizado_capital = models.BooleanField('Realizado Capital?', default=False)

    realizado_custeio = models.BooleanField('Realizado Custeio?', default=False)

    realizado_livre = models.BooleanField('Realizado Livre Aplicação?', default=False)

    carga_origem = models.ForeignKey('core.Arquivo', on_delete=models.SET_NULL,
                                     related_name='repasses_criados', blank=True, null=True)

    carga_origem_linha_id = models.PositiveSmallIntegerField('Id da linha de carga', default=0, blank=True, null=True)

    class Meta:
        verbose_name = 'Repasse'
        verbose_name_plural = 'Repasses'

    def __str__(self):
        return f'Repasse<val_capital: {self.valor_capital}, val_custeio: {self.valor_custeio}>'

    @property
    def valor_total(self):
        return self.valor_capital + self.valor_custeio

    @property
    def valor_realizado(self):
        return self.realizado_capital + self.realizado_custeio + self.realizado_livre

    @classmethod
    def repasses_pendentes_da_acao_associacao_no_periodo(cls, acao_associacao, periodo, conta_associacao=None):

        dataset = cls.objects.filter(acao_associacao=acao_associacao).filter(status='PENDENTE').filter(periodo=periodo)

        if conta_associacao:
            dataset = dataset.filter(conta_associacao=conta_associacao)

        return dataset.all()


auditlog.register(Repasse)
