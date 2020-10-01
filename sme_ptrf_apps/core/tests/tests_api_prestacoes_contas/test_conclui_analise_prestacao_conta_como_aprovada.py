import json
import pytest

from freezegun import freeze_time
from datetime import date

from model_bakery import baker
from rest_framework import status

from ...models import PrestacaoConta

pytestmark = pytest.mark.django_db


@pytest.fixture
def prestacao_conta_em_analise(periodo, associacao):
    return baker.make(
        'PrestacaoConta',
        periodo=periodo,
        associacao=associacao,
        data_recebimento=date(2020, 10, 1),
        status=PrestacaoConta.STATUS_EM_ANALISE
    )


@freeze_time('2020-09-01')
def test_api_conclui_analise_prestacao_conta_aprovada(client, prestacao_conta_em_analise, conta_associacao):
    payload = {
        'devolucao_tesouro': True,
        'analises_de_conta_da_prestacao': [
            {
                'conta_associacao': f'{conta_associacao.uuid}',
                'data_extrato': '2020-07-01',
                'saldo_extrato': 100.00,
            },
        ],
        'resultado_analise': PrestacaoConta.STATUS_APROVADA
    }

    url = f'/api/prestacoes-contas/{prestacao_conta_em_analise.uuid}/concluir-analise/'

    response = client.patch(url, data=json.dumps(payload), content_type='application/json')

    assert response.status_code == status.HTTP_200_OK

    prestacao_atualizada = PrestacaoConta.by_uuid(prestacao_conta_em_analise.uuid)
    assert prestacao_atualizada.status == PrestacaoConta.STATUS_APROVADA, 'Status deveria ter passado para APROVADA.'
    assert prestacao_atualizada.data_ultima_analise == date(2020, 9, 1), 'Data de última análise não atualizada.'
    assert prestacao_atualizada.devolucao_tesouro, 'Devolução ao tesouro não atualizado.'
    assert prestacao_atualizada.analises_de_conta_da_prestacao.exists(), 'Não gravou a análise de conta'
    assert prestacao_atualizada.analises_de_conta_da_prestacao.first().data_extrato == date(2020, 7,
                                                                                            1), 'Não atualizou a data do extrato.'
    assert prestacao_atualizada.analises_de_conta_da_prestacao.first().saldo_extrato == 100.00, 'Não atualizou a saldo do extrato.'
