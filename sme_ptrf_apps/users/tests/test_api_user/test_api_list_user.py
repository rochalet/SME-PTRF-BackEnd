import pytest

pytestmark = pytest.mark.django_db

def test_lista_usuarios(
        jwt_authenticated_client_u,
        usuario_para_teste,
        usuario_3,
        visao_ue,
        visao_dre,
        visao_sme,
        permissao1,
        permissao2,
        grupo_1,
        grupo_2):

    response = jwt_authenticated_client_u.get("/api/usuarios/?visao=DRE", content_type='application/json')
    result = response.json()
    esperado = [
        {
            'id': usuario_3.id,
            'username': usuario_3.username,
            'email': usuario_3.email,
            'name': usuario_3.name,
            'url': f'http://testserver/api/esqueci-minha-senha/{usuario_3.username}/',
            'e_servidor': usuario_3.e_servidor,
            'groups': [{'id': grupo_2.id, 'name': grupo_2.name, 'descricao': grupo_2.descricao}]
        }
    ]
    assert result == esperado


def test_filtro_por_grupo_lista_usuarios(
        jwt_authenticated_client_u2,
        usuario_2,
        usuario_3,
        visao_ue,
        visao_dre,
        visao_sme,
        permissao1,
        permissao2,
        grupo_1,
        grupo_2):

    response = jwt_authenticated_client_u2.get(
        f"/api/usuarios/?visao=DRE&groups__id={grupo_2.id}", content_type='application/json')
    result = response.json()
    esperado = [
        {
            'id': usuario_3.id,
            'username': '7218198',
            'email': 'sme8198@amcom.com.br',
            'name': 'Arthur Marques',
            'url': 'http://testserver/api/esqueci-minha-senha/7218198/',
            'e_servidor': usuario_3.e_servidor,
            'groups': [
                {
                   'id': grupo_2.id,
                   'name': 'grupo2',
                   'descricao': 'Descrição grupo 2'
                }
            ]
        }
    ]
    assert result == esperado


def test_filtro_por_nome_lista_usuarios(
        jwt_authenticated_client_u2,
        usuario_2,
        usuario_3,
        visao_ue,
        visao_dre,
        visao_sme,
        permissao1,
        permissao2,
        grupo_1,
        grupo_2):

    response = jwt_authenticated_client_u2.get(f"/api/usuarios/?visao=DRE&search=Arth", content_type='application/json')
    result = response.json()
    esperado = [
        {'id': usuario_3.id,
         'username': '7218198',
         'email': 'sme8198@amcom.com.br',
         'name': 'Arthur Marques',
         'url': 'http://testserver/api/esqueci-minha-senha/7218198/',
         'e_servidor': usuario_3.e_servidor,
         'groups': [
             {
                'id': grupo_2.id,
                'name': 'grupo2',
                'descricao': 'Descrição grupo 2'}]
         }
    ]
    assert result == esperado


def test_lista_usuarios_por_unidade(
        jwt_authenticated_client_u,
        usuario_para_teste,
        usuario_2,
        usuario_3,
        associacao,
        grupo_1,
        grupo_2):

    response = jwt_authenticated_client_u.get(f"/api/usuarios/?associacao_uuid={associacao.uuid}", content_type='application/json')
    result = response.json()
    esperado = [
        {
            'id': usuario_3.id,
            'name': 'Arthur Marques',
            'e_servidor': True,
            'url': 'http://testserver/api/esqueci-minha-senha/7218198/',
            'username': '7218198',
            'email': 'sme8198@amcom.com.br',
            'groups': [
                {
                    'descricao': 'Descrição grupo 2',
                    'id': grupo_2.id,
                    'name': 'grupo2'
                }],
        },
        {
            'id': usuario_para_teste.id,
            'name': 'LUCIA HELENA',
            'e_servidor': False,
            'url': 'http://testserver/api/esqueci-minha-senha/7210418/',
            'username': '7210418',
            'email': 'luh@gmail.com',
            'groups': [
                {
                    'descricao': 'Descrição grupo 1',
                    'id': grupo_1.id,
                    'name': 'grupo1'
                }],
        }

    ]
    print(result)
    assert result == esperado
