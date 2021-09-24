import json

import pytest

from rest_framework import status


pytestmark = pytest.mark.django_db


def test_api_get_solicitacoes_acerto_de_um_documento_nao_por_conta(
    jwt_authenticated_client_a,
    tipo_documento_prestacao_conta_ata,
    tipo_acerto_documento_assinatura,
    analise_documento_prestacao_conta_2020_1_ata_ajuste,
    solicitacao_acerto_documento_ata
):
    analise_prestacao = analise_documento_prestacao_conta_2020_1_ata_ajuste.analise_prestacao_conta
    prestacao_conta = analise_prestacao.prestacao_conta

    resultado_esperado = {
        'uuid': f'{analise_documento_prestacao_conta_2020_1_ata_ajuste.uuid}',
        'id': analise_documento_prestacao_conta_2020_1_ata_ajuste.id,
        'resultado': 'AJUSTE',
        'conta_associacao': None,
        'analise_prestacao_conta': f'{analise_prestacao.uuid}',
        'documento': 'Cópia da ata da prestação de contas',
        'tipo_documento_prestacao_conta': {
            'uuid': f'{tipo_documento_prestacao_conta_ata.uuid}',
            'id': tipo_documento_prestacao_conta_ata.id,
            'nome': tipo_documento_prestacao_conta_ata.nome,
            'documento_por_conta': False,
        },
        'solicitacoes_de_ajuste_da_analise': [
            {
                'analise_documento': f'{analise_documento_prestacao_conta_2020_1_ata_ajuste.uuid}',
                'tipo_acerto': {'id': tipo_acerto_documento_assinatura.id,
                                'nome': 'Enviar com '
                                        'assinatura',
                                'uuid': f'{tipo_acerto_documento_assinatura.uuid}'},
                'id': solicitacao_acerto_documento_ata.id,
                'uuid': f'{solicitacao_acerto_documento_ata.uuid}'
            },
        ],
    }

    url = f'/api/prestacoes-contas/{prestacao_conta.uuid}/analises-de-documento/?analise_documento={analise_documento_prestacao_conta_2020_1_ata_ajuste.uuid}'
    response = jwt_authenticated_client_a.get(url, content_type='application/json')

    result = json.loads(response.content)

    assert response.status_code == status.HTTP_200_OK
    assert result == resultado_esperado


def test_api_get_solicitacoes_acerto_de_um_documento_por_conta(
    jwt_authenticated_client_a,
    tipo_documento_prestacao_conta_declaracao,
    tipo_acerto_documento_assinatura,
    conta_associacao_cartao,
    analise_documento_prestacao_conta_2020_1_declaracao_cartao_ajuste,
    solicitacao_acerto_documento_declaracao_cartao,
):
    analise_prestacao = analise_documento_prestacao_conta_2020_1_declaracao_cartao_ajuste.analise_prestacao_conta
    prestacao_conta = analise_prestacao.prestacao_conta

    resultado_esperado = {
        'uuid': f'{analise_documento_prestacao_conta_2020_1_declaracao_cartao_ajuste.uuid}',
        'id': analise_documento_prestacao_conta_2020_1_declaracao_cartao_ajuste.id,
        'resultado': 'AJUSTE',
        'conta_associacao': {
            'nome': 'Cartão',
            'uuid': f'{conta_associacao_cartao.uuid}'
        },
        'analise_prestacao_conta': f'{analise_prestacao.uuid}',
        'documento': 'Declaração XPTO Cartão',
        'tipo_documento_prestacao_conta': {
            'uuid': f'{tipo_documento_prestacao_conta_declaracao.uuid}',
            'id': tipo_documento_prestacao_conta_declaracao.id,
            'nome': tipo_documento_prestacao_conta_declaracao.nome,
            'documento_por_conta': True,
        },
        'solicitacoes_de_ajuste_da_analise': [
            {
                'analise_documento': f'{analise_documento_prestacao_conta_2020_1_declaracao_cartao_ajuste.uuid}',
                'tipo_acerto': {'id': tipo_acerto_documento_assinatura.id,
                                'nome': 'Enviar com '
                                        'assinatura',
                                'uuid': f'{tipo_acerto_documento_assinatura.uuid}'},
                'id': solicitacao_acerto_documento_declaracao_cartao.id,
                'uuid': f'{solicitacao_acerto_documento_declaracao_cartao.uuid}'
            },
        ],
    }

    url = f'/api/prestacoes-contas/{prestacao_conta.uuid}/analises-de-documento/?analise_documento={analise_documento_prestacao_conta_2020_1_declaracao_cartao_ajuste.uuid}'
    response = jwt_authenticated_client_a.get(url, content_type='application/json')

    result = json.loads(response.content)

    assert response.status_code == status.HTTP_200_OK
    assert result == resultado_esperado