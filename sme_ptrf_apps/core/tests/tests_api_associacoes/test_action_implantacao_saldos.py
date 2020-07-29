import json

import pytest
from rest_framework import status

from ...models import Associacao

pytestmark = pytest.mark.django_db


def test_get_permite_implantacao_ok(client, associacao, periodo_anterior):
    response = client.get(f'/api/associacoes/{associacao.uuid}/permite-implantacao-saldos/',
                          content_type='application/json')
    result = json.loads(response.content)

    esperado = {
        'permite_implantacao': True,
        'erro': '',
        'mensagem': 'Os saldos podem ser implantados normalmente.'
    }

    assert response.status_code == status.HTTP_200_OK
    assert result == esperado


def test_get_permite_implantacao_sem_periodo_inicial_definido(client, associacao_sem_periodo_inicial,
                                                              periodo_anterior):
    response = client.get(f'/api/associacoes/{associacao_sem_periodo_inicial.uuid}/permite-implantacao-saldos/',
                          content_type='application/json')
    result = json.loads(response.content)

    esperado = {
        'permite_implantacao': False,
        'erro': 'periodo_inicial_nao_definido',
        'mensagem': 'Período inicial não foi definido para essa associação. Verifique com o administrador.'
    }

    assert response.status_code == status.HTTP_200_OK
    assert result == esperado


def test_get_permite_implantacao_com_prestacao_contas(client, associacao, periodo_anterior, prestacao_conta_iniciada,
                                                      acao_associacao_role_cultural, conta_associacao):
    response = client.get(f'/api/associacoes/{associacao.uuid}/permite-implantacao-saldos/',
                          content_type='application/json')
    result = json.loads(response.content)

    esperado = {
        'permite_implantacao': False,
        'erro': 'prestacao_de_contas_existente',
        'mensagem': 'Os saldos não podem ser implantados, já existe uma prestação de contas da associação.'
    }

    assert response.status_code == status.HTTP_200_OK
    assert result == esperado


def test_retrieve_implanta_saldos_saldos_ainda_nao_implantados(client, associacao, periodo_anterior):
    response = client.get(f'/api/associacoes/{associacao.uuid}/implantacao-saldos/',
                          content_type='application/json')
    result = json.loads(response.content)

    esperado = {
        'associacao': f'{associacao.uuid}',
        'periodo': {
            'referencia': '2019.1',
            'data_inicio_realizacao_despesas': '2019-01-01',
            'data_fim_realizacao_despesas': '2019-08-31',
            'referencia_por_extenso': '1° repasse de 2019',
            'uuid': f'{periodo_anterior.uuid}'
        },
        'saldos': [],
    }

    assert response.status_code == status.HTTP_200_OK
    assert result == esperado


def test_retrieve_implanta_saldos_saldos_ja_implantados(client, associacao, periodo_anterior,
                                                        fechamento_periodo_anterior_role_implantado,
                                                        acao_associacao_role_cultural,
                                                        conta_associacao):
    response = client.get(f'/api/associacoes/{associacao.uuid}/implantacao-saldos/',
                          content_type='application/json')
    result = json.loads(response.content)

    esperado = {
        'associacao': f'{associacao.uuid}',
        'periodo': {
            'referencia': '2019.1',
            'data_inicio_realizacao_despesas': '2019-01-01',
            'data_fim_realizacao_despesas': '2019-08-31',
            'referencia_por_extenso': '1° repasse de 2019',
            'uuid': f'{periodo_anterior.uuid}'
        },
        'saldos': [
            {
                'acao_associacao': {
                    'id': acao_associacao_role_cultural.id,
                    'uuid': f'{acao_associacao_role_cultural.uuid}',
                    'nome': acao_associacao_role_cultural.acao.nome
                },
                'conta_associacao': {
                    'uuid': f'{conta_associacao.uuid}',
                    'nome': f'{conta_associacao.tipo_conta.nome}'
                },
                'aplicacao': 'CAPITAL',
                'saldo': 1000.0
            },
            {
                'acao_associacao': {
                    'id': acao_associacao_role_cultural.id,
                    'uuid': f'{acao_associacao_role_cultural.uuid}',
                    'nome': acao_associacao_role_cultural.acao.nome
                },
                'conta_associacao': {
                    'uuid': f'{conta_associacao.uuid}',
                    'nome': f'{conta_associacao.tipo_conta.nome}'
                },
                'aplicacao': 'CUSTEIO',
                'saldo': 2000.0
            }
        ],
    }

    assert response.status_code == status.HTTP_200_OK
    assert result == esperado


def test_retrieve_implanta_saldos_sem_periodo_inicial_definido(client, associacao_sem_periodo_inicial,
                                                               periodo_anterior):
    response = client.get(f'/api/associacoes/{associacao_sem_periodo_inicial.uuid}/implantacao-saldos/',
                          content_type='application/json')
    result = json.loads(response.content)

    esperado = {
        'erro': 'periodo_inicial_nao_definido',
        'mensagem': 'Período inicial não foi definido para essa associação. Verifique com o administrador.'
    }

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert result == esperado


def test_post_implanta_saldos_com_prestacao_contas(client, associacao, periodo_anterior, prestacao_conta_iniciada,
                                                   acao_associacao_role_cultural, conta_associacao):
    payload = {
        'saldos': [
            {
                'acao_associacao': f'{acao_associacao_role_cultural.uuid}',
                'conta_associacao': f'{conta_associacao.uuid}',
                'aplicacao': 'CAPITAL',
                'saldo': 1000.0
            },
        ],
    }

    response = client.post(f'/api/associacoes/{associacao.uuid}/implanta-saldos/', data=json.dumps(payload),
                           content_type='application/json')
    result = json.loads(response.content)

    esperado = {
        'erro': 'prestacao_de_contas_existente',
        'mensagem': 'Os saldos não podem ser implantados, já existe uma prestação de contas da associação.'
    }

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert result == esperado


def test_post_implanta_saldos_sem_prestacao_contas(client, associacao, periodo_anterior, acao_associacao_role_cultural,
                                                   conta_associacao):
    payload = {
        'saldos': [
            {
                'acao_associacao': f'{acao_associacao_role_cultural.uuid}',
                'conta_associacao': f'{conta_associacao.uuid}',
                'aplicacao': 'CAPITAL',
                'saldo': 1000.0
            },
            {
                'acao_associacao': f'{acao_associacao_role_cultural.uuid}',
                'conta_associacao': f'{conta_associacao.uuid}',
                'aplicacao': 'CUSTEIO',
                'saldo': 2000.0
            },
        ],
    }

    response = client.post(f'/api/associacoes/{associacao.uuid}/implanta-saldos/', data=json.dumps(payload),
                           content_type='application/json')
    result = json.loads(response.content)

    esperado = {'associacao': f'{associacao.uuid}',
                'periodo': {'data_fim_realizacao_despesas': '2019-08-31',
                            'data_inicio_realizacao_despesas': '2019-01-01',
                            'referencia': '2019.1',
                            'referencia_por_extenso': '1° repasse de 2019',
                            'uuid': f'{periodo_anterior.uuid}'},
                'saldos': [
                    {
                        'acao_associacao': f'{acao_associacao_role_cultural.uuid}',
                        'aplicacao': 'CAPITAL',
                        'conta_associacao': f'{conta_associacao.uuid}',
                        'saldo': 1000.0
                    },
                    {
                        'acao_associacao': f'{acao_associacao_role_cultural.uuid}',
                        'aplicacao': 'CUSTEIO',
                        'conta_associacao': f'{conta_associacao.uuid}',
                        'saldo': 2000.0
                    }
                ]
                }

    assert response.status_code == status.HTTP_200_OK
    assert result == esperado

    assert Associacao.by_uuid(associacao.uuid).fechamentos_associacao.exists()
    implantacao = Associacao.by_uuid(associacao.uuid).fechamentos_associacao.first()
    assert implantacao.status == 'IMPLANTACAO'
    assert implantacao.total_receitas_capital == 1000.0
    assert implantacao.total_receitas_custeio == 2000.0
    assert implantacao.conta_associacao == conta_associacao
    assert implantacao.acao_associacao == acao_associacao_role_cultural
    assert implantacao.saldo_reprogramado_capital == 1000.0
    assert implantacao.saldo_reprogramado_custeio == 2000.0


def test_post_implanta_saldos_ja_existente(client, associacao, periodo_anterior, acao_associacao_role_cultural,
                                           conta_associacao, fechamento_periodo_anterior_role_implantado):
    payload = {
        'saldos': [
            {
                'acao_associacao': f'{acao_associacao_role_cultural.uuid}',
                'conta_associacao': f'{conta_associacao.uuid}',
                'aplicacao': 'CAPITAL',
                'saldo': 1000.0
            },
        ],
    }

    response = client.post(f'/api/associacoes/{associacao.uuid}/implanta-saldos/', data=json.dumps(payload),
                           content_type='application/json')
    result = json.loads(response.content)

    esperado = {'associacao': f'{associacao.uuid}',
                'periodo': {'data_fim_realizacao_despesas': '2019-08-31',
                            'data_inicio_realizacao_despesas': '2019-01-01',
                            'referencia': '2019.1',
                            'referencia_por_extenso': '1° repasse de 2019',
                            'uuid': f'{periodo_anterior.uuid}'},
                'saldos': [{'acao_associacao': f'{acao_associacao_role_cultural.uuid}',
                            'aplicacao': 'CAPITAL',
                            'conta_associacao': f'{conta_associacao.uuid}',
                            'saldo': 1000.0}]}

    assert response.status_code == status.HTTP_200_OK
    assert result == esperado

    assert Associacao.by_uuid(associacao.uuid).fechamentos_associacao.exists()
    assert Associacao.by_uuid(associacao.uuid).fechamentos_associacao.count() == 1


def test_post_implanta_saldos_duplicados(client, associacao, periodo_anterior, acao_associacao_role_cultural,
                                         conta_associacao):
    payload = {
        'saldos': [
            {
                'acao_associacao': f'{acao_associacao_role_cultural.uuid}',
                'conta_associacao': f'{conta_associacao.uuid}',
                'aplicacao': 'CAPITAL',
                'saldo': 1000.0
            },
            {
                'acao_associacao': f'{acao_associacao_role_cultural.uuid}',
                'conta_associacao': f'{conta_associacao.uuid}',
                'aplicacao': 'CAPITAL',
                'saldo': 100.0
            }
        ],
    }

    response = client.post(f'/api/associacoes/{associacao.uuid}/implanta-saldos/', data=json.dumps(payload),
                           content_type='application/json')
    result = json.loads(response.content)

    esperado = {
        'erro': 'informacoes_repetidas',
        'mensagem': 'Existem valores repetidos de Ação, Conta e Aplicação. Verifique.'
    }

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert result == esperado

    assert Associacao.by_uuid(associacao.uuid).fechamentos_associacao.count() == 0


def test_retrieve_implanta_saldos_saldos_ja_implantados_livre_aplicacao(client, associacao, periodo_anterior,
                                                                        fechamento_periodo_anterior_role_implantado_com_livre_aplicacao,
                                                                        acao_associacao_role_cultural,
                                                                        conta_associacao):
    response = client.get(f'/api/associacoes/{associacao.uuid}/implantacao-saldos/',
                          content_type='application/json')
    result = json.loads(response.content)

    esperado = {
        'associacao': f'{associacao.uuid}',
        'periodo': {
            'referencia': '2019.1',
            'data_inicio_realizacao_despesas': '2019-01-01',
            'data_fim_realizacao_despesas': '2019-08-31',
            'referencia_por_extenso': '1° repasse de 2019',
            'uuid': f'{periodo_anterior.uuid}'
        },
        'saldos': [
            {
                'acao_associacao': {
                    'id': acao_associacao_role_cultural.id,
                    'uuid': f'{acao_associacao_role_cultural.uuid}',
                    'nome': acao_associacao_role_cultural.acao.nome
                },
                'conta_associacao': {
                    'uuid': f'{conta_associacao.uuid}',
                    'nome': f'{conta_associacao.tipo_conta.nome}'
                },
                'aplicacao': 'CAPITAL',
                'saldo': 1000.0
            },
            {
                'acao_associacao': {
                    'id': acao_associacao_role_cultural.id,
                    'uuid': f'{acao_associacao_role_cultural.uuid}',
                    'nome': acao_associacao_role_cultural.acao.nome
                },
                'conta_associacao': {
                    'uuid': f'{conta_associacao.uuid}',
                    'nome': f'{conta_associacao.tipo_conta.nome}'
                },
                'aplicacao': 'CUSTEIO',
                'saldo': 2000.0
            },
            {
                'acao_associacao': {
                    'id': acao_associacao_role_cultural.id,
                    'uuid': f'{acao_associacao_role_cultural.uuid}',
                    'nome': acao_associacao_role_cultural.acao.nome
                },
                'conta_associacao': {
                    'uuid': f'{conta_associacao.uuid}',
                    'nome': f'{conta_associacao.tipo_conta.nome}'
                },
                'aplicacao': 'LIVRE',
                'saldo': 3000.0
            }
        ],
    }

    assert response.status_code == status.HTTP_200_OK
    assert result == esperado


def test_post_implanta_saldos_sem_prestacao_contas_com_livre_utilizacao(client, associacao, periodo_anterior,
                                                                        acao_associacao_role_cultural,
                                                                        conta_associacao):
    payload = {
        'saldos': [
            {
                'acao_associacao': f'{acao_associacao_role_cultural.uuid}',
                'conta_associacao': f'{conta_associacao.uuid}',
                'aplicacao': 'CAPITAL',
                'saldo': 1000.0
            },
            {
                'acao_associacao': f'{acao_associacao_role_cultural.uuid}',
                'conta_associacao': f'{conta_associacao.uuid}',
                'aplicacao': 'CUSTEIO',
                'saldo': 2000.0
            },
            {
                'acao_associacao': f'{acao_associacao_role_cultural.uuid}',
                'conta_associacao': f'{conta_associacao.uuid}',
                'aplicacao': 'LIVRE',
                'saldo': 3000.0
            },
        ],
    }

    response = client.post(f'/api/associacoes/{associacao.uuid}/implanta-saldos/', data=json.dumps(payload),
                           content_type='application/json')
    result = json.loads(response.content)

    esperado = {'associacao': f'{associacao.uuid}',
                'periodo': {'data_fim_realizacao_despesas': '2019-08-31',
                            'data_inicio_realizacao_despesas': '2019-01-01',
                            'referencia': '2019.1',
                            'referencia_por_extenso': '1° repasse de 2019',
                            'uuid': f'{periodo_anterior.uuid}'},
                'saldos': [
                    {
                        'acao_associacao': f'{acao_associacao_role_cultural.uuid}',
                        'aplicacao': 'CAPITAL',
                        'conta_associacao': f'{conta_associacao.uuid}',
                        'saldo': 1000.0
                    },
                    {
                        'acao_associacao': f'{acao_associacao_role_cultural.uuid}',
                        'aplicacao': 'CUSTEIO',
                        'conta_associacao': f'{conta_associacao.uuid}',
                        'saldo': 2000.0
                    },
                    {
                        'acao_associacao': f'{acao_associacao_role_cultural.uuid}',
                        'aplicacao': 'LIVRE',
                        'conta_associacao': f'{conta_associacao.uuid}',
                        'saldo': 3000.0
                    }
                ]
                }

    assert response.status_code == status.HTTP_200_OK
    assert result == esperado

    assert Associacao.by_uuid(associacao.uuid).fechamentos_associacao.exists()
    implantacao = Associacao.by_uuid(associacao.uuid).fechamentos_associacao.first()
    assert implantacao.status == 'IMPLANTACAO'
    assert implantacao.total_receitas_capital == 1000.0
    assert implantacao.total_receitas_custeio == 2000.0
    assert implantacao.total_receitas_livre == 3000.0
    assert implantacao.conta_associacao == conta_associacao
    assert implantacao.acao_associacao == acao_associacao_role_cultural
    assert implantacao.saldo_reprogramado_capital == 1000.0
    assert implantacao.saldo_reprogramado_custeio == 2000.0
    assert implantacao.saldo_reprogramado_livre == 3000.0
