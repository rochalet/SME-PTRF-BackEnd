import json

import pytest
from rest_framework import status

pytestmark = pytest.mark.django_db

def test_retrieve_processo_associacao(
        jwt_authenticated_client,
        processo_associacao_123456_2019):

    response = jwt_authenticated_client.get(
        f'/api/processos-associacao/{processo_associacao_123456_2019.uuid}/', content_type='application/json')
    result = json.loads(response.content)
    esperado = {
        'uuid': f'{processo_associacao_123456_2019.uuid}',
        'associacao':
            {
                'id': processo_associacao_123456_2019.associacao.id,
                'nome': processo_associacao_123456_2019.associacao.nome
            },
        'criado_em': processo_associacao_123456_2019.criado_em.isoformat("T"),
        'alterado_em': processo_associacao_123456_2019.alterado_em.isoformat("T"),
        'numero_processo': processo_associacao_123456_2019.numero_processo,
        'ano': processo_associacao_123456_2019.ano,
    }

    assert response.status_code == status.HTTP_200_OK
    assert result == esperado

