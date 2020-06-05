from decimal import Decimal

from ..models import FechamentoPeriodo, Associacao, AcaoAssociacao, ContaAssociacao
from ...despesas.models import RateioDespesa
from ...despesas.tipos_aplicacao_recurso import APLICACAO_CUSTEIO
from ...receitas.models import Receita


def saldos_insuficientes_para_rateios(rateios, periodo, exclude_despesa=None):
    def sumariza_rateios_por_acao(rateios):
        totalizador_aplicacoes = {
            'CUSTEIO': Decimal(0.00),
            'CAPITAL': Decimal(0.00)
        }
        totalizador_acoes = dict()
        totalizador_contas = dict()
        for rateio in rateios:
            acao_key = rateio['acao_associacao']
            conta_key = rateio['conta_associacao']
            aplicacao = rateio['aplicacao_recurso']

            if not acao_key or not aplicacao: continue

            if acao_key not in totalizador_acoes:
                totalizador_acoes[acao_key] = totalizador_aplicacoes

            totalizador_acoes[acao_key][aplicacao] += Decimal(rateio['valor_rateio'])

            if conta_key and conta_key not in totalizador_contas:
                totalizador_contas[conta_key] = Decimal(0.00)

            if conta_key:
                totalizador_contas[conta_key] += Decimal(rateio['valor_rateio'])

        return totalizador_acoes, totalizador_contas

    gastos_por_acao, gastos_por_conta = sumariza_rateios_por_acao(rateios)

    saldos_insuficientes = []

    for conta_associacao_uuid, gasto_conta_associacao in gastos_por_conta.items():
        conta_associacao = ContaAssociacao.by_uuid(conta_associacao_uuid)
        saldos_conta = info_conta_associacao_no_periodo(conta_associacao, periodo, exclude_despesa=exclude_despesa)

        saldo_conta = saldos_conta['saldo_atual_custeio'] + saldos_conta['saldo_atual_capital']
        if saldo_conta < gasto_conta_associacao:
            saldo_insuficiente = {
                'conta': conta_associacao.tipo_conta.nome,
                'saldo_disponivel': saldo_conta,
                'total_rateios': gasto_conta_associacao
            }
            saldos_insuficientes.append(saldo_insuficiente)

    if saldos_insuficientes:
        return {
            'tipo_saldo': 'CONTA',
            'saldos_insuficientes': saldos_insuficientes
        }

    for acao_associacao_uuid, gastos_acao_associacao in gastos_por_acao.items():
        acao_associacao = AcaoAssociacao.by_uuid(acao_associacao_uuid)
        saldos_acao = info_acao_associacao_no_periodo(acao_associacao, periodo, exclude_despesa=exclude_despesa)

        for aplicacao, saldo_atual_key in (('CUSTEIO', 'saldo_atual_custeio'), ('CAPITAL', 'saldo_atual_capital')):
            if not gastos_acao_associacao[aplicacao]: continue

            if saldos_acao[saldo_atual_key] < gastos_acao_associacao[aplicacao]:
                saldo_insuficiente = {
                    'acao': acao_associacao.acao.nome,
                    'aplicacao': aplicacao,
                    'saldo_disponivel': saldos_acao[saldo_atual_key],
                    'total_rateios': gastos_acao_associacao[aplicacao]
                }
                saldos_insuficientes.append(saldo_insuficiente)

    return {
        'tipo_saldo': 'ACAO',
        'saldos_insuficientes': saldos_insuficientes
    }


def info_acao_associacao_no_periodo(acao_associacao, periodo, exclude_despesa=None, conta=None):
    def resultado_vazio():
        return {
            'saldo_anterior_custeio': 0,
            'receitas_no_periodo_custeio': 0,
            'repasses_no_periodo_custeio': 0,
            'despesas_no_periodo_custeio': 0,
            'saldo_atual_custeio': 0,
            'saldo_anterior_capital': 0,
            'receitas_no_periodo_capital': 0,
            'repasses_no_periodo_capital': 0,
            'despesas_no_periodo_capital': 0,
            'saldo_atual_capital': 0,
            'receitas_nao_conciliadas_custeio': 0,
            'receitas_nao_conciliadas_capital': 0,
            'despesas_nao_conciliadas_custeio': 0,
            'despesas_nao_conciliadas_capital': 0,
        }

    def fechamento_sumarizado_por_acao(fechamentos_periodo, conta=None):
        info = resultado_vazio()
        for fechamento_periodo in fechamentos_periodo:

            if conta and fechamento_periodo.conta_associacao != conta: continue

            info['saldo_anterior_custeio'] += fechamento_periodo.saldo_anterior_custeio
            info['receitas_no_periodo_custeio'] += fechamento_periodo.total_receitas_custeio
            info['repasses_no_periodo_custeio'] += fechamento_periodo.total_repasses_custeio
            info['despesas_no_periodo_custeio'] += fechamento_periodo.total_despesas_custeio
            info['saldo_atual_custeio'] += fechamento_periodo.saldo_reprogramado_custeio
            info['saldo_anterior_capital'] += fechamento_periodo.saldo_anterior_capital
            info['receitas_no_periodo_capital'] += fechamento_periodo.total_receitas_capital
            info['repasses_no_periodo_capital'] += fechamento_periodo.total_repasses_capital
            info['despesas_no_periodo_capital'] += fechamento_periodo.total_despesas_capital
            info['saldo_atual_capital'] += fechamento_periodo.saldo_reprogramado_capital
            info['receitas_nao_conciliadas_custeio'] += fechamento_periodo.total_receitas_nao_conciliadas_custeio
            info['receitas_nao_conciliadas_capital'] += fechamento_periodo.total_receitas_nao_conciliadas_capital
            info['despesas_nao_conciliadas_custeio'] += fechamento_periodo.total_despesas_nao_conciliadas_custeio
            info['despesas_nao_conciliadas_capital'] += fechamento_periodo.total_despesas_nao_conciliadas_capital

        return info

    def sumariza_receitas_do_periodo_e_acao(periodo, acao_associacao, info, conta=None):
        receitas = Receita.receitas_da_acao_associacao_no_periodo(acao_associacao=acao_associacao, periodo=periodo)

        for receita in receitas:
            if conta and receita.conta_associacao != conta: continue

            if receita.categoria_receita == APLICACAO_CUSTEIO:
                info['receitas_no_periodo_custeio'] += receita.valor
                info['saldo_atual_custeio'] += receita.valor
                info['repasses_no_periodo_custeio'] += receita.valor if receita.tipo_receita.e_repasse else 0
                info['receitas_nao_conciliadas_custeio'] += receita.valor if not receita.conferido else 0

            else:
                info['receitas_no_periodo_capital'] += receita.valor
                info['saldo_atual_capital'] += receita.valor
                info['repasses_no_periodo_capital'] += receita.valor if receita.tipo_receita.e_repasse else 0
                info['receitas_nao_conciliadas_capital'] += receita.valor if not receita.conferido else 0

        return info

    def sumariza_despesas_do_periodo_e_acao(periodo, acao_associacao, info, exclude_despesa=exclude_despesa,
                                            conta=None):
        rateios = RateioDespesa.rateios_da_acao_associacao_no_periodo(acao_associacao=acao_associacao, periodo=periodo,
                                                                      exclude_despesa=exclude_despesa)

        for rateio in rateios:
            if conta and rateio.conta_associacao != conta: continue

            if rateio.aplicacao_recurso == APLICACAO_CUSTEIO:
                info['despesas_no_periodo_custeio'] += rateio.valor_rateio
                info['saldo_atual_custeio'] -= rateio.valor_rateio
                info['despesas_nao_conciliadas_custeio'] += rateio.valor_rateio if not rateio.conferido else 0

            else:
                info['despesas_no_periodo_capital'] += rateio.valor_rateio
                info['saldo_atual_capital'] -= rateio.valor_rateio
                info['despesas_nao_conciliadas_capital'] += rateio.valor_rateio if not rateio.conferido else 0

        return info

    def periodo_aberto_sumarizado_por_acao(periodo, acao_associacao, conta=None):
        info = resultado_vazio()

        if not periodo or not periodo.periodo_anterior:
            return info

        fechamentos_periodo_anterior = FechamentoPeriodo.fechamentos_da_acao_no_periodo(acao_associacao=acao_associacao,
                                                                                        periodo=periodo.periodo_anterior)
        if fechamentos_periodo_anterior:
            sumario_periodo_anterior = fechamento_sumarizado_por_acao(fechamentos_periodo_anterior, conta=conta)
            info['saldo_anterior_capital'] = sumario_periodo_anterior['saldo_atual_capital']
            info['saldo_anterior_custeio'] = sumario_periodo_anterior['saldo_atual_custeio']
            info['saldo_atual_capital'] = info['saldo_anterior_capital']
            info['saldo_atual_custeio'] = info['saldo_anterior_custeio']

        info = sumariza_receitas_do_periodo_e_acao(periodo=periodo, acao_associacao=acao_associacao, info=info,
                                                   conta=conta)

        info = sumariza_despesas_do_periodo_e_acao(periodo=periodo, acao_associacao=acao_associacao, info=info,
                                                   conta=conta)

        return info

    fechamentos_periodo = FechamentoPeriodo.fechamentos_da_acao_no_periodo(acao_associacao=acao_associacao,
                                                                           periodo=periodo)
    if fechamentos_periodo:
        return fechamento_sumarizado_por_acao(fechamentos_periodo, conta=conta)
    else:
        return periodo_aberto_sumarizado_por_acao(periodo, acao_associacao, conta=conta)


def info_acoes_associacao_no_periodo(associacao_uuid, periodo, conta=None):
    acoes_associacao = Associacao.acoes_da_associacao(associacao_uuid=associacao_uuid)
    result = []
    for acao_associacao in acoes_associacao:
        info_acao = info_acao_associacao_no_periodo(acao_associacao=acao_associacao, periodo=periodo, conta=conta)
        info = {
            'acao_associacao_uuid': f'{acao_associacao.uuid}',
            'acao_associacao_nome': acao_associacao.acao.nome,

            'saldo_reprogramado': info_acao['saldo_anterior_custeio'] + info_acao['saldo_anterior_capital'],
            'saldo_reprogramado_capital': info_acao['saldo_anterior_capital'],
            'saldo_reprogramado_custeio': info_acao['saldo_anterior_custeio'],

            'receitas_no_periodo': info_acao['receitas_no_periodo_custeio'] + info_acao['receitas_no_periodo_capital'],

            'repasses_no_periodo': info_acao['repasses_no_periodo_custeio'] + info_acao['repasses_no_periodo_capital'],
            'repasses_no_periodo_capital': info_acao['repasses_no_periodo_capital'],
            'repasses_no_periodo_custeio': info_acao['repasses_no_periodo_custeio'],

            'outras_receitas_no_periodo': info_acao['receitas_no_periodo_custeio'] +
                                          info_acao['receitas_no_periodo_capital'] -
                                          info_acao['repasses_no_periodo_custeio'] -
                                          info_acao['repasses_no_periodo_capital'],

            'outras_receitas_no_periodo_capital': info_acao['receitas_no_periodo_capital'] -
                                                  info_acao['repasses_no_periodo_capital'],

            'outras_receitas_no_periodo_custeio': info_acao['receitas_no_periodo_custeio'] -
                                                  info_acao['repasses_no_periodo_custeio'],

            'despesas_no_periodo': info_acao['despesas_no_periodo_custeio'] + info_acao['despesas_no_periodo_capital'],
            'despesas_no_periodo_capital': info_acao['despesas_no_periodo_capital'],
            'despesas_no_periodo_custeio': info_acao['despesas_no_periodo_custeio'],

            'despesas_nao_conciliadas': info_acao['despesas_nao_conciliadas_custeio'] + info_acao['despesas_nao_conciliadas_capital'],
            'despesas_nao_conciliadas_capital': info_acao['despesas_nao_conciliadas_capital'],
            'despesas_nao_conciliadas_custeio': info_acao['despesas_nao_conciliadas_custeio'],

            'receitas_nao_conciliadas': info_acao['receitas_nao_conciliadas_custeio'] + info_acao['receitas_nao_conciliadas_capital'],
            'receitas_nao_conciliadas_capital': info_acao['receitas_nao_conciliadas_capital'],
            'receitas_nao_conciliadas_custeio': info_acao['receitas_nao_conciliadas_custeio'],

            'saldo_atual_custeio': info_acao['saldo_atual_custeio'],
            'saldo_atual_capital': info_acao['saldo_atual_capital'],
            'saldo_atual_total': info_acao['saldo_atual_custeio'] + info_acao['saldo_atual_capital'],
        }
        result.append(info)

    return result


def info_conta_associacao_no_periodo(conta_associacao, periodo, exclude_despesa=None):
    def resultado_vazio():
        return {
            'saldo_anterior_custeio': 0,
            'receitas_no_periodo_custeio': 0,
            'repasses_no_periodo_custeio': 0,
            'despesas_no_periodo_custeio': 0,
            'saldo_atual_custeio': 0,
            'saldo_anterior_capital': 0,
            'receitas_no_periodo_capital': 0,
            'repasses_no_periodo_capital': 0,
            'despesas_no_periodo_capital': 0,
            'saldo_atual_capital': 0,
        }

    def fechamento_sumarizado_por_conta(fechamentos_periodo):
        info = resultado_vazio()
        for fechamento_periodo in fechamentos_periodo:
            info['saldo_anterior_custeio'] += fechamento_periodo.saldo_anterior_custeio
            info['receitas_no_periodo_custeio'] += fechamento_periodo.total_receitas_custeio
            info['repasses_no_periodo_custeio'] += fechamento_periodo.total_repasses_custeio
            info['despesas_no_periodo_custeio'] += fechamento_periodo.total_despesas_custeio
            info['saldo_atual_custeio'] += fechamento_periodo.saldo_reprogramado_custeio
            info['saldo_anterior_capital'] += fechamento_periodo.saldo_anterior_capital
            info['receitas_no_periodo_capital'] += fechamento_periodo.total_receitas_capital
            info['repasses_no_periodo_capital'] += fechamento_periodo.total_repasses_capital
            info['despesas_no_periodo_capital'] += fechamento_periodo.total_despesas_capital
            info['saldo_atual_capital'] += fechamento_periodo.saldo_reprogramado_capital
        return info

    def sumariza_receitas_do_periodo_e_conta(periodo, conta_associacao, info):
        receitas = Receita.receitas_da_conta_associacao_no_periodo(conta_associacao=conta_associacao, periodo=periodo)

        for receita in receitas:
            if receita.categoria_receita == APLICACAO_CUSTEIO:
                info['receitas_no_periodo_custeio'] += receita.valor
                info['saldo_atual_custeio'] += receita.valor
                info['repasses_no_periodo_custeio'] += receita.valor if receita.tipo_receita.e_repasse else 0

            else:
                info['receitas_no_periodo_capital'] += receita.valor
                info['saldo_atual_capital'] += receita.valor
                info['repasses_no_periodo_capital'] += receita.valor if receita.tipo_receita.e_repasse else 0

        return info

    def sumariza_despesas_do_periodo_e_conta(periodo, conta_associacao, info, exclude_despesa=exclude_despesa):
        rateios = RateioDespesa.rateios_da_conta_associacao_no_periodo(conta_associacao=conta_associacao,
                                                                       periodo=periodo,
                                                                       exclude_despesa=exclude_despesa)

        for rateio in rateios:
            if rateio.aplicacao_recurso == APLICACAO_CUSTEIO:
                info['despesas_no_periodo_custeio'] += rateio.valor_rateio
                info['saldo_atual_custeio'] -= rateio.valor_rateio
            else:
                info['despesas_no_periodo_capital'] += rateio.valor_rateio
                info['saldo_atual_capital'] -= rateio.valor_rateio

        return info

    def periodo_aberto_sumarizado_por_conta(periodo, conta_associacao):
        info = resultado_vazio()

        if not periodo or not periodo.periodo_anterior:
            return info

        fechamentos_periodo_anterior = FechamentoPeriodo.fechamentos_da_conta_no_periodo(
            conta_associacao=conta_associacao,
            periodo=periodo.periodo_anterior)
        if fechamentos_periodo_anterior:
            sumario_periodo_anterior = fechamento_sumarizado_por_conta(fechamentos_periodo_anterior)
            info['saldo_anterior_capital'] = sumario_periodo_anterior['saldo_atual_capital']
            info['saldo_anterior_custeio'] = sumario_periodo_anterior['saldo_atual_custeio']
            info['saldo_atual_capital'] = info['saldo_anterior_capital']
            info['saldo_atual_custeio'] = info['saldo_anterior_custeio']

        info = sumariza_receitas_do_periodo_e_conta(periodo=periodo, conta_associacao=conta_associacao, info=info)

        info = sumariza_despesas_do_periodo_e_conta(periodo=periodo, conta_associacao=conta_associacao, info=info)

        return info

    fechamentos_periodo = FechamentoPeriodo.fechamentos_da_conta_no_periodo(conta_associacao=conta_associacao,
                                                                            periodo=periodo)
    if fechamentos_periodo:
        return fechamento_sumarizado_por_conta(fechamentos_periodo)
    else:
        return periodo_aberto_sumarizado_por_conta(periodo, conta_associacao)
