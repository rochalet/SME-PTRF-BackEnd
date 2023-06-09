import json
import pytest
import datetime
from freezegun import freeze_time
from datetime import date

from model_bakery import baker
from rest_framework import status

from ...models import PrestacaoConta

pytestmark = pytest.mark.django_db

@pytest.fixture
def prestacao_conta_2020_1_em_analise(periodo_2020_1, associacao):
    return baker.make(
        'PrestacaoConta',
        periodo=periodo_2020_1,
        associacao=associacao,
        data_recebimento=datetime.date(2020, 10, 1),
        status="EM_ANALISE"
    )


@pytest.fixture
def analise_prestacao_conta_2020_1_em_analise(prestacao_conta_2020_1_em_analise,):
    return baker.make(
        'AnalisePrestacaoConta',
        prestacao_conta=prestacao_conta_2020_1_em_analise,
    )

@pytest.fixture
def prestacao_conta_em_analise(periodo, associacao, analise_prestacao_conta_2020_1_em_analise):
    return baker.make(
        'PrestacaoConta',
        periodo=periodo,
        associacao=associacao,
        data_recebimento=date(2020, 10, 1),
        status=PrestacaoConta.STATUS_EM_ANALISE,
        analise_atual=analise_prestacao_conta_2020_1_em_analise
    )


@pytest.fixture
def periodo_anterior_01():
    return baker.make(
        'Periodo',
        referencia='2019.1',
        data_inicio_realizacao_despesas=date(2019, 1, 1),
        data_fim_realizacao_despesas=date(2019, 8, 31),
    )


@pytest.fixture
def periodo_01(periodo_anterior_01):
    return baker.make(
        'Periodo',
        referencia='2019.2',
        data_inicio_realizacao_despesas=date(2019, 9, 1),
        data_fim_realizacao_despesas=date(2019, 11, 30),
        data_prevista_repasse=date(2019, 10, 1),
        data_inicio_prestacao_contas=date(2019, 12, 1),
        data_fim_prestacao_contas=date(2019, 12, 5),
        periodo_anterior=periodo_anterior_01,
    )


@pytest.fixture
def prestacao_conta_01_pc_posterior(periodo_01, associacao, motivo_aprovacao_ressalva_x, motivo_reprovacao_x):
    return baker.make(
        'PrestacaoConta',
        id=1,
        periodo=periodo_01,
        associacao=associacao,
        data_recebimento=date(2020, 10, 1),
        data_ultima_analise=date(2020, 10, 1),
        motivos_reprovacao=[motivo_reprovacao_x, ],
        outros_motivos_reprovacao="Outros motivos reprovação",
        motivos_aprovacao_ressalva=[motivo_aprovacao_ressalva_x, ],
        outros_motivos_aprovacao_ressalva="Outros motivos",
        status='EM_ANALISE'

    )


@pytest.fixture
def prestacao_conta_02_pc_posterior(periodo, associacao, motivo_aprovacao_ressalva_x, motivo_reprovacao_x):
    return baker.make(
        'PrestacaoConta',
        id=2,
        periodo=periodo,
        associacao=associacao,
        data_recebimento=date(2020, 10, 2),
        data_ultima_analise=date(2020, 10, 2),
        motivos_reprovacao=[motivo_reprovacao_x, ],
        outros_motivos_reprovacao="Outros motivos reprovação",
        motivos_aprovacao_ressalva=[motivo_aprovacao_ressalva_x, ],
        outros_motivos_aprovacao_ressalva="Outros motivos")


@pytest.fixture
def despesa(associacao, tipo_documento, tipo_transacao):
    return baker.make(
        'Despesa',
        associacao=associacao,
        numero_documento='123456',
        data_documento=date(2020, 3, 10),
        tipo_documento=tipo_documento,
        cpf_cnpj_fornecedor='11.478.276/0001-04',
        nome_fornecedor='Fornecedor SA',
        tipo_transacao=tipo_transacao,
        data_transacao=date(2020, 3, 10),
        valor_total=100.00,
    )


@pytest.fixture
def tipo_devolucao_ao_tesouro():
    return baker.make('TipoDevolucaoAoTesouro', nome='Teste')


@freeze_time('2020-09-01')
def test_api_conclui_analise_prestacao_conta_devolvida(jwt_authenticated_client_a, prestacao_conta_em_analise,
                                                       conta_associacao, despesa, tipo_devolucao_ao_tesouro):
    payload = {
        'analises_de_conta_da_prestacao': [
            {
                'conta_associacao': f'{conta_associacao.uuid}',
                'data_extrato': '2020-07-01',
                'saldo_extrato': 100.00,
            },
        ],
        'resultado_analise': PrestacaoConta.STATUS_DEVOLVIDA,
        'data_limite_ue': '2020-07-21',
    }

    url = f'/api/prestacoes-contas/{prestacao_conta_em_analise.uuid}/concluir-analise/'

    response = jwt_authenticated_client_a.patch(url, data=json.dumps(payload), content_type='application/json')

    assert response.status_code == status.HTTP_200_OK

    prestacao_atualizada = PrestacaoConta.by_uuid(prestacao_conta_em_analise.uuid)
    assert prestacao_atualizada.status == PrestacaoConta.STATUS_DEVOLVIDA, 'Status deveria ter passado para APROVADA_RESSALVA.'
    assert prestacao_atualizada.devolucoes_da_prestacao.exists(), 'Não gravou o registro de devolução da PC.'
    assert prestacao_atualizada.devolucoes_da_prestacao.first().data_limite_ue == date(2020, 7,
                                                                                       21), 'Não gravou a data limite.'


def test_api_conclui_analise_prestacao_conta_aprovada_ressalva_exige_data_limite(jwt_authenticated_client_a,
                                                                                 prestacao_conta_em_analise,
                                                                                 conta_associacao):
    payload = {
        'analises_de_conta_da_prestacao': [
            {
                'conta_associacao': f'{conta_associacao.uuid}',
                'data_extrato': '2020-07-01',
                'saldo_extrato': 100.00,
            },
        ],
        'resultado_analise': PrestacaoConta.STATUS_DEVOLVIDA,
    }
    url = f'/api/prestacoes-contas/{prestacao_conta_em_analise.uuid}/concluir-analise/'

    response = jwt_authenticated_client_a.patch(url, data=json.dumps(payload), content_type='application/json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    result = json.loads(response.content)

    result_esperado = {
        'uuid': f'{prestacao_conta_em_analise.uuid}',
        'erro': 'falta_de_informacoes',
        'operacao': 'concluir-analise',
        'mensagem': 'Para concluir como DEVOLVIDA é necessário informar o campo data_limite_ue.'
    }

    assert result == result_esperado, "Deveria ter retornado erro falta_de_informacoes."
