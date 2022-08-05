import json
import pytest
from rest_framework import status

pytestmark = pytest.mark.django_db


def test_api_valores_reprogramados_list(
    jwt_authenticated_client_dre,
    dre,
    unidade,
    unidade_valores_reprogramados,
    associacao,
    associacao_2,
    periodo_anterior,
    fechamento_conta_cheque_valores_reprogramados,
    fechamento_conta_cheque_valores_reprogramados_2,
    fechamento_conta_cartao_valores_reprogramados,
    fechamento_conta_cartao_valores_reprogramados_2,
    parametros_dre_valores_reprogramados
):
    response = jwt_authenticated_client_dre.get(
        f'/api/valores-reprogramados/?dre_uuid={dre.uuid}', content_type='application/json')

    result = json.loads(response.content)

    assert response.status_code == status.HTTP_200_OK
    assert len(result) == 2


def test_api_valores_reprogramados_lista_associacoes(
    jwt_authenticated_client_dre,
    dre,
    unidade,
    unidade_valores_reprogramados,
    associacao,
    associacao_2,
    associacao_3,
    periodo_anterior,
    fechamento_conta_cheque_valores_reprogramados,
    fechamento_conta_cheque_valores_reprogramados_2,
    fechamento_conta_cartao_valores_reprogramados,
    fechamento_conta_cartao_valores_reprogramados_2,
    parametros_dre_valores_reprogramados
):
    response = jwt_authenticated_client_dre.get(
        f'/api/valores-reprogramados/lista-associacoes/?dre_uuid={dre.uuid}', content_type='application/json')

    result = json.loads(response.content)

    assert response.status_code == status.HTTP_200_OK

    # Associacao 3 não entrará na lista pois não possui periodo inicial
    assert len(result['valores_reprogramados']) == 2

