from ..models import FechamentoPeriodo, Associacao
from ...receitas.models import Receita
from ...despesas.models import RateioDespesa
from ...despesas.tipos_aplicacao_recurso import APLICACAO_CUSTEIO, APLICACAO_CAPITAL


def info_acao_associacao_no_periodo(acao_associacao, periodo):
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

    def fechamento_sumarizado_por_acao(fechamentos_periodo):
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

    def sumariza_receitas_do_periodo_e_acao(periodo, acao_associacao, info):
        receitas = Receita.receitas_da_acao_associacao_no_periodo(acao_associacao=acao_associacao, periodo=periodo)

        for receita in receitas:
            info['receitas_no_periodo_custeio'] += receita.valor
            info['saldo_atual_custeio'] += receita.valor

        return info

    def sumariza_despesas_do_periodo_e_acao(periodo, acao_associacao, info):
        rateios = RateioDespesa.rateios_da_acao_associacao_no_periodo(acao_associacao=acao_associacao, periodo=periodo)

        for rateio in rateios:
            if rateio.aplicacao_recurso == APLICACAO_CUSTEIO:
                info['despesas_no_periodo_custeio'] += rateio.valor_rateio
                info['saldo_atual_custeio'] -= rateio.valor_rateio
            else:
                info['despesas_no_periodo_capital'] += rateio.valor_rateio
                info['saldo_atual_capital'] -= rateio.valor_rateio

        return info

    def periodo_aberto_sumarizado_por_acao(periodo, acao_associacao):
        info = resultado_vazio()

        if not periodo or not periodo.periodo_anterior:
            return info

        fechamentos_periodo_anterior = FechamentoPeriodo.fechamentos_da_acao_no_periodo(acao_associacao=acao_associacao,
                                                                                        periodo=periodo.periodo_anterior)
        if fechamentos_periodo_anterior:
            sumario_periodo_anterior = fechamento_sumarizado_por_acao(fechamentos_periodo_anterior)
            info['saldo_anterior_capital'] = sumario_periodo_anterior['saldo_atual_capital']
            info['saldo_anterior_custeio'] = sumario_periodo_anterior['saldo_atual_custeio']
            info['saldo_atual_capital'] = info['saldo_anterior_capital']
            info['saldo_atual_custeio'] = info['saldo_anterior_custeio']

        info = sumariza_receitas_do_periodo_e_acao(periodo=periodo, acao_associacao=acao_associacao, info=info)

        info = sumariza_despesas_do_periodo_e_acao(periodo=periodo, acao_associacao=acao_associacao, info=info)

        return info

    fechamentos_periodo = FechamentoPeriodo.fechamentos_da_acao_no_periodo(acao_associacao=acao_associacao,
                                                                           periodo=periodo)
    if fechamentos_periodo:
        return fechamento_sumarizado_por_acao(fechamentos_periodo)
    else:
        return periodo_aberto_sumarizado_por_acao(periodo, acao_associacao)


def info_acoes_associacao_no_periodo(associacao_uuid, periodo):
    acoes_associacao = Associacao.acoes_da_associacao(associacao_uuid=associacao_uuid)
    result = []
    for acao_associacao in acoes_associacao:
        info_acao = info_acao_associacao_no_periodo(acao_associacao=acao_associacao, periodo=periodo)
        info = {
            'acao_associacao_uuid': f'{acao_associacao.uuid}',
            'acao_associacao_nome': acao_associacao.acao.nome,
            'saldo_reprogramado': info_acao['saldo_anterior_custeio'] + info_acao['saldo_anterior_capital'],
            'receitas_no_periodo': info_acao['receitas_no_periodo_custeio'] + info_acao['receitas_no_periodo_capital'],
            'repasses_no_periodo': info_acao['repasses_no_periodo_custeio'] + info_acao['repasses_no_periodo_capital'],
            'despesas_no_periodo': info_acao['despesas_no_periodo_custeio'] + info_acao['despesas_no_periodo_capital'],
            'saldo_atual_custeio': info_acao['saldo_atual_custeio'],
            'saldo_atual_capital': info_acao['saldo_atual_capital'],
            'saldo_atual_total': info_acao['saldo_atual_custeio'] + info_acao['saldo_atual_capital'],
        }
        result.append(info)

    return result