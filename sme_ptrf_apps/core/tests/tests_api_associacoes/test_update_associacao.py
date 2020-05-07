import json

import pytest
from rest_framework import status

from ...models import Associacao
from ...api.serializers.associacao_serializer import AssociacaoCreateSerializer

pytestmark = pytest.mark.django_db


def test_api_update_associacao(client, associacao):
    payload = {
        "nome": "Nome alterado",
        "presidente_associacao_nome": "Presidente alterado"
    }
    response = client.put(f'/api/associacoes/{associacao.uuid}/', data=json.dumps(payload),
                          content_type='application/json')

    registro_alterado = Associacao.objects.get(uuid=associacao.uuid)

    assert response.status_code == status.HTTP_200_OK
    assert registro_alterado.nome == 'Nome alterado'
    assert registro_alterado.presidente_associacao_nome == 'Presidente alterado'