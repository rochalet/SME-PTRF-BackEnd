import json

import pytest
from model_bakery import baker
from rest_framework import status

pytestmark = pytest.mark.django_db


@pytest.fixture
def dre_1():
    return baker.make('Unidade', codigo_eol='00001', tipo_unidade='DRE', nome='DRE 1')


@pytest.fixture
def dre_2():
    return baker.make('Unidade', codigo_eol='00002', tipo_unidade='DRE', nome='DRE 2')


@pytest.fixture
def ceu_vassouras_dre_1(dre_1):
    return baker.make('Unidade', codigo_eol='00011', dre=dre_1, tipo_unidade='CEU', nome='Escola Vassouras')


@pytest.fixture
def emef_mendes_dre_2(dre_2):
    return baker.make('Unidade', codigo_eol='00022', dre=dre_2, tipo_unidade='EMEF', nome='Escola Mendes')


@pytest.fixture
def associacao_valenca_ceu_vassouras_dre_1(ceu_vassouras_dre_1, periodo_anterior):
    return baker.make(
        'Associacao',
        nome='Associacao Valença',
        cnpj='52.302.275/0001-83',
        unidade=ceu_vassouras_dre_1,
        status_regularidade='PENDENTE'
    )


@pytest.fixture
def associacao_pinheiros_emef_mendes_dre_2(emef_mendes_dre_2, periodo_anterior):
    return baker.make(
        'Associacao',
        nome='Associação Pinheiros',
        cnpj='05.861.145/0001-09',
        unidade=emef_mendes_dre_2,
        status_regularidade='REGULAR'
    )


def test_api_list_associacoes_todas(client, associacao_valenca_ceu_vassouras_dre_1,
                                    associacao_pinheiros_emef_mendes_dre_2):
    response = client.get(f'/api/associacoes/', content_type='application/json')
    result = json.loads(response.content)

    result_esperado = [
        {
            'uuid': f'{associacao_valenca_ceu_vassouras_dre_1.uuid}',
            'nome': associacao_valenca_ceu_vassouras_dre_1.nome,
            'unidade': {
                'uuid': f'{associacao_valenca_ceu_vassouras_dre_1.unidade.uuid}',
                'codigo_eol': associacao_valenca_ceu_vassouras_dre_1.unidade.codigo_eol,
                'nome_com_tipo': associacao_valenca_ceu_vassouras_dre_1.unidade.nome_com_tipo
            },
            'status_regularidade': associacao_valenca_ceu_vassouras_dre_1.status_regularidade,
        },
        {
            'uuid': f'{associacao_pinheiros_emef_mendes_dre_2.uuid}',
            'nome': associacao_pinheiros_emef_mendes_dre_2.nome,
            'unidade': {
                'uuid': f'{associacao_pinheiros_emef_mendes_dre_2.unidade.uuid}',
                'codigo_eol': associacao_pinheiros_emef_mendes_dre_2.unidade.codigo_eol,
                'nome_com_tipo': associacao_pinheiros_emef_mendes_dre_2.unidade.nome_com_tipo
            },
            'status_regularidade': associacao_pinheiros_emef_mendes_dre_2.status_regularidade,
        },
    ]

    assert response.status_code == status.HTTP_200_OK
    assert result == result_esperado


def test_api_list_associacoes_de_uma_dre(client, associacao_valenca_ceu_vassouras_dre_1,
                                         associacao_pinheiros_emef_mendes_dre_2):
    response = client.get(
        f'/api/associacoes/?unidade__dre__uuid={associacao_valenca_ceu_vassouras_dre_1.unidade.dre.uuid}',
        content_type='application/json')
    result = json.loads(response.content)

    result_esperado = [
        {
            'uuid': f'{associacao_valenca_ceu_vassouras_dre_1.uuid}',
            'nome': associacao_valenca_ceu_vassouras_dre_1.nome,
            'unidade': {
                'uuid': f'{associacao_valenca_ceu_vassouras_dre_1.unidade.uuid}',
                'codigo_eol': associacao_valenca_ceu_vassouras_dre_1.unidade.codigo_eol,
                'nome_com_tipo': associacao_valenca_ceu_vassouras_dre_1.unidade.nome_com_tipo
            },
            'status_regularidade': associacao_valenca_ceu_vassouras_dre_1.status_regularidade,
        },
    ]

    assert response.status_code == status.HTTP_200_OK
    assert result == result_esperado


def test_api_list_associacoes_pelo_nome_associacao_ignorando_acentos(client, associacao_valenca_ceu_vassouras_dre_1,
                                                                     associacao_pinheiros_emef_mendes_dre_2):
    response = client.get(f'/api/associacoes/?nome=valenca', content_type='application/json')
    result = json.loads(response.content)

    result_esperado = [
        {
            'uuid': f'{associacao_valenca_ceu_vassouras_dre_1.uuid}',
            'nome': associacao_valenca_ceu_vassouras_dre_1.nome,
            'unidade': {
                'uuid': f'{associacao_valenca_ceu_vassouras_dre_1.unidade.uuid}',
                'codigo_eol': associacao_valenca_ceu_vassouras_dre_1.unidade.codigo_eol,
                'nome_com_tipo': associacao_valenca_ceu_vassouras_dre_1.unidade.nome_com_tipo
            },
            'status_regularidade': associacao_valenca_ceu_vassouras_dre_1.status_regularidade,
        },
    ]

    assert response.status_code == status.HTTP_200_OK
    assert result == result_esperado


def test_api_list_associacoes_pelo_nome_escola(client, associacao_valenca_ceu_vassouras_dre_1,
                                               associacao_pinheiros_emef_mendes_dre_2):
    response = client.get(f'/api/associacoes/?nome=vassouras', content_type='application/json')
    result = json.loads(response.content)

    result_esperado = [
        {
            'uuid': f'{associacao_valenca_ceu_vassouras_dre_1.uuid}',
            'nome': associacao_valenca_ceu_vassouras_dre_1.nome,
            'unidade': {
                'uuid': f'{associacao_valenca_ceu_vassouras_dre_1.unidade.uuid}',
                'codigo_eol': associacao_valenca_ceu_vassouras_dre_1.unidade.codigo_eol,
                'nome_com_tipo': associacao_valenca_ceu_vassouras_dre_1.unidade.nome_com_tipo
            },
            'status_regularidade': associacao_valenca_ceu_vassouras_dre_1.status_regularidade,
        },
    ]

    assert response.status_code == status.HTTP_200_OK
    assert result == result_esperado


def test_api_list_associacoes_pelo_status_regularidade(client, associacao_valenca_ceu_vassouras_dre_1,
                                                       associacao_pinheiros_emef_mendes_dre_2):
    response = client.get(f'/api/associacoes/?status_regularidade=PENDENTE', content_type='application/json')
    result = json.loads(response.content)

    result_esperado = [
        {
            'uuid': f'{associacao_valenca_ceu_vassouras_dre_1.uuid}',
            'nome': associacao_valenca_ceu_vassouras_dre_1.nome,
            'unidade': {
                'uuid': f'{associacao_valenca_ceu_vassouras_dre_1.unidade.uuid}',
                'codigo_eol': associacao_valenca_ceu_vassouras_dre_1.unidade.codigo_eol,
                'nome_com_tipo': associacao_valenca_ceu_vassouras_dre_1.unidade.nome_com_tipo
            },
            'status_regularidade': associacao_valenca_ceu_vassouras_dre_1.status_regularidade,
        },
    ]

    assert response.status_code == status.HTTP_200_OK
    assert result == result_esperado


def test_api_list_associacoes_pelo_tipo_unidade(client, associacao_valenca_ceu_vassouras_dre_1,
                                                associacao_pinheiros_emef_mendes_dre_2):
    response = client.get(f'/api/associacoes/?unidade__tipo_unidade=CEU', content_type='application/json')
    result = json.loads(response.content)

    result_esperado = [
        {
            'uuid': f'{associacao_valenca_ceu_vassouras_dre_1.uuid}',
            'nome': associacao_valenca_ceu_vassouras_dre_1.nome,
            'unidade': {
                'uuid': f'{associacao_valenca_ceu_vassouras_dre_1.unidade.uuid}',
                'codigo_eol': associacao_valenca_ceu_vassouras_dre_1.unidade.codigo_eol,
                'nome_com_tipo': associacao_valenca_ceu_vassouras_dre_1.unidade.nome_com_tipo
            },
            'status_regularidade': associacao_valenca_ceu_vassouras_dre_1.status_regularidade,
        },
    ]

    assert response.status_code == status.HTTP_200_OK
    assert result == result_esperado