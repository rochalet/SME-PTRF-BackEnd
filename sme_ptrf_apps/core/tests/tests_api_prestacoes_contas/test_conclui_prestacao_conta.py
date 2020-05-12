import json

import pytest
from rest_framework import status

from ...api.serializers import PrestacaoContaLookUpSerializer
from ...models import PrestacaoConta

pytestmark = pytest.mark.django_db


def test_api_conclui_prestacao_conta(client, prestacao_conta_iniciada):
    url = f'/api/prestacoes-contas/{prestacao_conta_iniciada.uuid}/concluir/'

    observacoes = "Teste observações."
    payload = {
        "observacoes": observacoes
    }

    response = client.patch(url, data=json.dumps(payload), content_type='application/json')

    result = json.loads(response.content)


    prestacao_concluida = PrestacaoConta.by_uuid(uuid=prestacao_conta_iniciada.uuid)
    result_esperado = PrestacaoContaLookUpSerializer(
        prestacao_concluida,
        many=False).data

    # Converto os campos UUIDs em strings para que a comparação funcione
    result_esperado['conta_associacao_uuid'] = f'{result_esperado["conta_associacao_uuid"]}'
    result_esperado['periodo_uuid'] = f'{result_esperado["periodo_uuid"]}'

    assert response.status_code == status.HTTP_200_OK
    assert result == result_esperado, "Não retornou a prestação de contas esperada."

    assert prestacao_concluida.conciliado, "Flag conciliado deveria ser True."
    assert prestacao_concluida.observacoes == observacoes, "Não gravou as observações."
    assert prestacao_concluida.conciliado_em is not None, "Deveria haver data da última conciliação."


def test_api_conclui_prestacao_conta_sem_observacoes(client, prestacao_conta_iniciada):
    url = f'/api/prestacoes-contas/{prestacao_conta_iniciada.uuid}/concluir/'

    payload = {
        "observacoes": ""
    }

    response = client.patch(url, data=json.dumps(payload), content_type='application/json')

    assert response.status_code == status.HTTP_200_OK, "Deve aceitar o campo observacoes vazio."


def test_api_conclui_prestacao_conta_sem_payload(client, prestacao_conta_iniciada):
    url = f'/api/prestacoes-contas/{prestacao_conta_iniciada.uuid}/concluir/'

    response = client.patch(url, content_type='application/json')

    assert response.status_code == status.HTTP_200_OK, "Deve aceitar o campo observacoes vazio."