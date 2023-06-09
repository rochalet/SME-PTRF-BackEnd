import pytest
from rest_framework import status

from sme_ptrf_apps.despesas.models import Despesa, RateioDespesa
from sme_ptrf_apps.receitas.models import Receita
import json

pytestmark = pytest.mark.django_db


def test_api_deve_conciliar_transacao_despesa(
    jwt_authenticated_client_a,
    acao_associacao_role_cultural,
    despesa_2020_1,
    rateio_despesa_2020_role_nao_conferido,
    rateio_despesa_2020_ptrf_conferido,
    periodo_2020_1,
    conta_associacao_cartao

):

    url = f'/api/conciliacoes/conciliar-despesa/?periodo={periodo_2020_1.uuid}'
    url = f'{url}&conta_associacao={conta_associacao_cartao.uuid}'
    url = f'{url}&transacao={despesa_2020_1.uuid}'

    response = jwt_authenticated_client_a.patch(url, content_type='application/json')

    despesa_conciliada = Despesa.by_uuid(despesa_2020_1.uuid)
    rateio_conciliado = RateioDespesa.by_uuid(rateio_despesa_2020_role_nao_conferido.uuid)

    assert response.status_code == status.HTTP_200_OK

    assert despesa_conciliada.conferido, "Despesa deveria ter sido marcada como conferida."
    assert rateio_conciliado.conferido, "Rateio deveria ter sido marcado como conferido."
    assert rateio_conciliado.periodo_conciliacao == periodo_2020_1, "Rateio deveria ter sido vinculada ao período."


def test_api_nao_deve_conciliar_transacao_receita(
    jwt_authenticated_client_a,
    acao_associacao_role_cultural,
    receita_2020_1_ptrf_repasse_conferida,
    receita_2020_1_role_outras_nao_conferida,
    periodo_2020_1,
    conta_associacao_cartao

):

    url = f'/api/conciliacoes/conciliar-despesa/?periodo={periodo_2020_1.uuid}'
    url = f'{url}&conta_associacao={conta_associacao_cartao.uuid}'
    url = f'{url}&transacao={receita_2020_1_role_outras_nao_conferida.uuid}'

    response = jwt_authenticated_client_a.patch(url, content_type='application/json')
    result = json.loads(response.content)

    receita_conciliada = Receita.by_uuid(receita_2020_1_role_outras_nao_conferida.uuid)
    esperado = {
        "erro": "Gasto não encontrado.",
        "mensagem": f"O objeto de gasto para o uuid {receita_conciliada.uuid} não foi encontrado na base."
    }

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert result == esperado


def test_api_deve_desconciliar_transacao_despesa(
    jwt_authenticated_client_a,
    acao_associacao_role_cultural,
    despesa_2020_1,
    rateio_despesa_2020_role_nao_conferido,
    rateio_despesa_2020_ptrf_conferido,
    periodo_2020_1,
    conta_associacao_cartao

):

    url = f'/api/conciliacoes/desconciliar-despesa/?periodo={periodo_2020_1.uuid}'
    url = f'{url}&conta_associacao={conta_associacao_cartao.uuid}'
    url = f'{url}&transacao={despesa_2020_1.uuid}'

    response = jwt_authenticated_client_a.patch(url, content_type='application/json')

    despesa_desconciliada = Despesa.by_uuid(despesa_2020_1.uuid)
    rateio_desconciliado = RateioDespesa.by_uuid(rateio_despesa_2020_ptrf_conferido.uuid)

    assert response.status_code == status.HTTP_200_OK

    assert not despesa_desconciliada.conferido, "Despesa deveria ter sido desconciliada."
    assert not rateio_desconciliado.conferido, "Rateio deveria ter sido desconciliado."
    assert rateio_desconciliado.periodo_conciliacao is None, "Período deveria ter sido desvinculado."


def test_api_nao_deve_desconciliar_transacao_receita(
    jwt_authenticated_client_a,
    acao_associacao_role_cultural,
    receita_2020_1_ptrf_repasse_conferida,
    receita_2020_1_role_outras_nao_conferida,
    periodo_2020_1,
    conta_associacao_cartao

):

    url = f'/api/conciliacoes/desconciliar-despesa/'
    url = f'{url}?conta_associacao={conta_associacao_cartao.uuid}'
    url = f'{url}&transacao={receita_2020_1_ptrf_repasse_conferida.uuid}'

    response = jwt_authenticated_client_a.patch(url, content_type='application/json')
    result = json.loads(response.content)

    receita_desconciliada = Receita.by_uuid(receita_2020_1_ptrf_repasse_conferida.uuid)
    esperado = {
        "erro": "Gasto não encontrado.",
        "mensagem": f"O objeto de Gasto para o uuid {receita_desconciliada.uuid} não foi encontrado na base."
    }

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert result == esperado

