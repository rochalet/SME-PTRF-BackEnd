import json

import pytest
from rest_framework import status

pytestmark = pytest.mark.django_db


def test_api_retrieve_ata_associacao(client, associacao, ata_2020_1_cheque_aprovada):
    response = client.get(f'/api/atas-associacao/{ata_2020_1_cheque_aprovada.uuid}/', content_type='application/json')
    result = json.loads(response.content)

    result_esperado = {
        'associacao': {'cnpj': '52.302.275/0001-83',
                       'nome': 'Escola Teste',
                       'unidade': {'nome': 'Escola Teste', 'tipo_unidade': 'CEU'},
                       'uuid': f'{ata_2020_1_cheque_aprovada.associacao.uuid}'},
        'cargo_presidente_reuniao': 'Presidente',
        'cargo_secretaria_reuniao': 'Secretária',
        'comentarios': 'Teste',
        'conta_associacao': {'agencia': '12345',
                             'banco_nome': 'Banco do Brasil',
                             'nome': 'Cheque',
                             'numero_conta': '123456-x',
                             'uuid': f'{ata_2020_1_cheque_aprovada.conta_associacao.uuid}'},
        'convocacao': 'PRIMEIRA',
        'data_reuniao': '2020-07-01',
        'local_reuniao': 'Escola Teste',
        'nome': 'Ata de Apresentação da prestação de contas',
        'parecer_conselho': 'APROVADA',
        'periodo': {'data_fim_realizacao_despesas': '2020-06-30',
                    'data_inicio_realizacao_despesas': '2020-01-01',
                    'referencia': '2020.1',
                    'uuid': f'{ata_2020_1_cheque_aprovada.periodo.uuid}'},
        'presidente_reuniao': 'José',
        'prestacao_conta': f'{ata_2020_1_cheque_aprovada.prestacao_conta.uuid}',
        'secretario_reuniao': 'Ana',
        'tipo_ata': 'APRESENTACAO',
        'tipo_reuniao': 'ORDINARIA',
        'uuid': f'{ata_2020_1_cheque_aprovada.uuid}'
    }
    assert response.status_code == status.HTTP_200_OK
    assert result == result_esperado
