import json

import pytest
from model_bakery import baker
from rest_framework import status

pytestmark = pytest.mark.django_db


@pytest.fixture
def dre_01():
    return baker.make(
        'Unidade',
        uuid='f92d2caf-d71f-4ed0-87b2-6d326fb648a7',
        codigo_eol='108500',
        tipo_unidade='DRE',
        nome='GUAIANASES',
        sigla='G'
    )


@pytest.fixture
def unidade_paulo_camilhier_florencano_dre_1(dre_01):
    return baker.make(
        'Unidade',
        uuid="ae06f0f7-0aca-41d6-94c3-dea20558627d",
        codigo_eol="000086",
        tipo_unidade="EMEI",
        nome="PAULO CAMILHIER FLORENCANO",
        sigla="",
        dre=dre_01,
        email="",
        telefone="",
        tipo_logradouro="",
        logradouro="",
        numero="",
        complemento="",
        bairro="",
        cep="",
        diretor_nome="",
        dre_cnpj="",
        dre_diretor_regional_rf="",
        dre_diretor_regional_nome="",
        dre_designacao_portaria="",
        dre_designacao_ano=""
    )


def test_api_list_unidades_todas(
    jwt_authenticated_client_a,
    unidade_paulo_camilhier_florencano_dre_1,
    dre_01,
    dre,
    unidade,
    associacao
):
    response = jwt_authenticated_client_a.get(f'/api/unidades/', content_type='application/json')
    result = json.loads(response.content)

    result_esperado = [
        {
            'codigo_eol': '99999',
            'nome': 'DRE teste',
            'nome_com_tipo': 'DRE DRE teste',
            'tipo_unidade': 'DRE',
            'uuid': str(dre.uuid),
            'associacao_nome': '',
            'associacao_uuid': '',
            'visao': 'DRE',
        },
        {
            'codigo_eol': '123456',
            'nome': 'Escola Teste',
            'nome_com_tipo': 'CEU Escola Teste',
            'tipo_unidade': 'CEU',
            'uuid': str(unidade.uuid),
            'nome_dre': 'DRE teste',
            'associacao_nome': 'Escola Teste',
            'associacao_uuid': f'{associacao.uuid}',
            'visao': 'UE',
        },
        {
            "codigo_eol": f'{dre_01.codigo_eol}',
            "nome": f'{dre_01.nome}',
            "nome_com_tipo": f'{dre_01.nome_com_tipo}',
            'tipo_unidade': 'DRE',
            "uuid": f'{dre_01.uuid}',
            'associacao_nome': '',
            'associacao_uuid': '',
            'visao': 'DRE',
        },
        {
            "codigo_eol": f'{unidade_paulo_camilhier_florencano_dre_1.codigo_eol}',
            "nome": f'{unidade_paulo_camilhier_florencano_dre_1.nome}',
            "nome_com_tipo": f'{unidade_paulo_camilhier_florencano_dre_1.nome_com_tipo}',
            'tipo_unidade': f'{unidade_paulo_camilhier_florencano_dre_1.tipo_unidade}',
            "uuid": f'{unidade_paulo_camilhier_florencano_dre_1.uuid}',
            'nome_dre': unidade_paulo_camilhier_florencano_dre_1.dre.nome,
            'associacao_nome': '',
            'associacao_uuid': '',
            'visao': 'UE',
        }

    ]

    assert response.status_code == status.HTTP_200_OK
    assert result == result_esperado


def test_api_list_unidades_por_nome(
    jwt_authenticated_client_a,
    unidade_paulo_camilhier_florencano_dre_1,
    dre_01,
    dre,
    unidade
):
    response = jwt_authenticated_client_a.get(f'/api/unidades/?search=Escola', content_type='application/json')
    result = json.loads(response.content)

    result_esperado = [
        {
            'codigo_eol': '123456',
            'nome_dre': 'DRE teste',
            'nome': 'Escola Teste',
            'nome_com_tipo': 'CEU Escola Teste',
            'tipo_unidade': 'CEU',
            'uuid': str(unidade.uuid),
            'associacao_nome': '',
            'associacao_uuid': '',
            'visao': 'UE'
        },

    ]

    assert response.status_code == status.HTTP_200_OK
    assert result == result_esperado


def test_api_list_unidades_por_codigo_eol(
    jwt_authenticated_client_a,
    unidade_paulo_camilhier_florencano_dre_1,
    dre_01,
    dre,
    unidade
):
    response = jwt_authenticated_client_a.get(f'/api/unidades/?search=123456', content_type='application/json')
    result = json.loads(response.content)

    result_esperado = [
        {
            'codigo_eol': '123456',
            'nome_dre': 'DRE teste',
            'nome': 'Escola Teste',
            'nome_com_tipo': 'CEU Escola Teste',
            'tipo_unidade': 'CEU',
            'uuid': str(unidade.uuid),
            'associacao_nome': '',
            'associacao_uuid': '',
            'visao': 'UE'
        },

    ]

    assert response.status_code == status.HTTP_200_OK
    assert result == result_esperado


def test_api_list_unidades_filtro_por_tipo(
    jwt_authenticated_client_a,
    unidade_paulo_camilhier_florencano_dre_1,
    dre_01,
    dre,
    unidade
):
    response = jwt_authenticated_client_a.get(f'/api/unidades/?tipo_unidade=DRE', content_type='application/json')
    result = json.loads(response.content)

    result_esperado = [
        {
            'codigo_eol': '99999',
            'nome': 'DRE teste',
            'nome_com_tipo': 'DRE DRE teste',
            'tipo_unidade': 'DRE',
            'uuid': str(dre.uuid),
            'associacao_nome': '',
            'associacao_uuid': '',
            'visao': 'DRE'
        },
        {
            "uuid": f'{dre_01.uuid}',
            "codigo_eol": f'{dre_01.codigo_eol}',
            "nome": f'{dre_01.nome}',
            "nome_com_tipo": f'{dre_01.nome_com_tipo}',
            'tipo_unidade': 'DRE',
            'associacao_nome': '',
            'associacao_uuid': '',
            'visao': 'DRE'
        },
    ]

    assert response.status_code == status.HTTP_200_OK
    assert result == result_esperado


def test_api_list_unidades_por_dre(
    jwt_authenticated_client_a,
    unidade_paulo_camilhier_florencano_dre_1,
    dre_01,
    dre,
    unidade
):
    response = jwt_authenticated_client_a.get(f'/api/unidades/?dre__uuid={dre.uuid}', content_type='application/json')
    result = json.loads(response.content)

    result_esperado = [
        {
            'codigo_eol': '123456',
            'nome_dre': 'DRE teste',
            'nome': 'Escola Teste',
            'nome_com_tipo': 'CEU Escola Teste',
            'tipo_unidade': 'CEU',
            'uuid': str(unidade.uuid),
            'associacao_nome': '',
            'associacao_uuid': '',
            'visao': 'UE'
        },
    ]

    assert response.status_code == status.HTTP_200_OK
    assert result == result_esperado
