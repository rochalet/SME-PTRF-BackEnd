import json

import pytest

from model_bakery import baker

from sme_ptrf_apps.core.services.notificacao_services import formata_data
from sme_ptrf_apps.core.choices import MembroEnum, RepresentacaoCargo
from sme_ptrf_apps.core.models import Notificacao
from django.contrib.auth.models import Permission
from sme_ptrf_apps.users.models import Grupo

pytestmark = pytest.mark.django_db

@pytest.fixture
def notificacao(usuario_permissao_associacao):
    return baker.make(
        'Notificacao',
        tipo=Notificacao.TIPO_NOTIFICACAO_INFORMACAO,
        categoria=Notificacao.CATEGORIA_NOTIFICACAO_COMENTARIO_PC,
        remetente=Notificacao.REMETENTE_NOTIFICACAO_DRE,
        titulo="Documentos Faltantes",
        descricao="Documentos Faltantes na prestação de contas",
        usuario=usuario_permissao_associacao
    )


@pytest.fixture
def notificacao2(usuario_permissao_associacao):
    return baker.make(
        'Notificacao',
        tipo=Notificacao.TIPO_NOTIFICACAO_URGENTE,
        categoria=Notificacao.CATEGORIA_NOTIFICACAO_ELABORACAO_PC,
        remetente=Notificacao.REMETENTE_NOTIFICACAO_SISTEMA,
        lido=True,
        titulo="Documentos Faltantes 2",
        descricao="Documentos Faltantes na prestação de contas 2",
        usuario=usuario_permissao_associacao
    )


def test_quantidade_de_nao_lidos(jwt_authenticated_client_a, notificacao):
    response = jwt_authenticated_client_a.get(
        f'/api/notificacoes/quantidade-nao-lidos/', content_type='application/json')
    result = json.loads(response.content)
    assert result['quantidade_nao_lidos'] == 1


def test_lista_notificacoes(jwt_authenticated_client_a, notificacao):
    response = jwt_authenticated_client_a.get(
        f'/api/notificacoes/', content_type='application/json')
    result = json.loads(response.content)
    esperado = {
            'count': 1,
            'links': {'next': None,
                      'previous': None},
            'page': 1,
            'page_size': 10,
            'results': [
                {
                    'data': formata_data(notificacao.criado_em.date()),
                    'infos': [
                        {
                            'uuid': str(notificacao.uuid),
                            'unidade': None,
                            'titulo': notificacao.titulo,
                            'descricao': notificacao.descricao,
                            'lido': notificacao.lido,
                            'periodo': None,
                            'hora': notificacao.hora.strftime("%H:%M"),
                            'tipo': Notificacao.TIPO_NOTIFICACAO_NOMES[notificacao.tipo],
                            'remetente': Notificacao.REMETENTE_NOTIFICACAO_NOMES[notificacao.remetente],
                            'categoria': Notificacao.CATEGORIA_NOTIFICACAO_NOMES[notificacao.categoria]
                        }
                    ]
                }
            ]
        }

    assert result == esperado


def test_filtro_lido(jwt_authenticated_client_a, notificacao, notificacao2):
    response = jwt_authenticated_client_a.get(
        f'/api/notificacoes/?lido=True', content_type='application/json')
    result = json.loads(response.content)
    esperado = {
            'count': 1,
            'links': {'next': None,
                      'previous': None},
            'page': 1,
            'page_size': 10,
            'results': [
                {
                    'data': formata_data(notificacao2.criado_em.date()),
                    'infos': [
                        {
                            'uuid': str(notificacao2.uuid),
                            'unidade': None,
                            'titulo': notificacao2.titulo,
                            'descricao': notificacao2.descricao,
                            'lido': notificacao2.lido,
                            'periodo': None,
                            'hora': notificacao2.hora.strftime("%H:%M"),
                            'tipo': Notificacao.TIPO_NOTIFICACAO_NOMES[notificacao2.tipo],
                            'remetente': Notificacao.REMETENTE_NOTIFICACAO_NOMES[notificacao2.remetente],
                            'categoria': Notificacao.CATEGORIA_NOTIFICACAO_NOMES[notificacao2.categoria]
                        }
                    ]
                }
            ]

    }

    assert result == esperado


def test_filtro_tipo(jwt_authenticated_client_a, notificacao, notificacao2):
    response = jwt_authenticated_client_a.get(
        f'/api/notificacoes/?tipo={notificacao2.tipo}', content_type='application/json')
    result = json.loads(response.content)
    esperado = {
            'count': 1,
            'links': {'next': None,
                      'previous': None},
            'page': 1,
            'page_size': 10,
            'results': [
                {
                    'data': formata_data(notificacao2.criado_em.date()),
                    'infos': [
                        {
                            'uuid': str(notificacao2.uuid),
                            'unidade': None,
                            'titulo': notificacao2.titulo,
                            'descricao': notificacao2.descricao,
                            'lido': notificacao2.lido,
                            'periodo': None,
                            'hora': notificacao2.hora.strftime("%H:%M"),
                            'tipo': Notificacao.TIPO_NOTIFICACAO_NOMES[notificacao2.tipo],
                            'remetente': Notificacao.REMETENTE_NOTIFICACAO_NOMES[notificacao2.remetente],
                            'categoria': Notificacao.CATEGORIA_NOTIFICACAO_NOMES[notificacao2.categoria]
                        }
                    ]
                }
            ]
    }

    assert result == esperado

@pytest.fixture
def permissao_notificar():
    return Permission.objects.filter(codename='recebe_notificacao_comentario_em_pc').first()

@pytest.fixture
def grupo_com_permissao_notificar(permissao_notificar):
    g = Grupo.objects.create(name="grupo1")
    g.permissions.add(permissao_notificar)
    g.descricao = "Descrição grupo 1"
    g.save()
    return g

@pytest.fixture
def usuario_presidente(unidade, grupo_com_permissao_notificar):
    from django.contrib.auth import get_user_model
    senha = 'Sgp8888'
    login = '7218888'
    email = 'sme88@amcom.com.br'
    User = get_user_model()
    user = User.objects.create_user(username=login, password=senha, email=email)
    user.unidades.add(unidade)
    user.groups.add(grupo_com_permissao_notificar)
    user.save()
    return user


@pytest.fixture
def usuario_vice_presidente(unidade, grupo_com_permissao_notificar):
    from django.contrib.auth import get_user_model
    senha = 'Sgp9999'
    login = '7219999'
    email = 'sme99@amcom.com.br'
    User = get_user_model()
    user = User.objects.create_user(username=login, password=senha, email=email)
    user.unidades.add(unidade)
    user.groups.add(grupo_com_permissao_notificar)
    user.save()
    return user

@pytest.fixture
def usuario_apenas_com_permissao(grupo_com_permissao_notificar):
    from django.contrib.auth import get_user_model
    senha = 'Sgp0418'
    login = '6605656'
    email = 'sme@amcom.com.br'
    User = get_user_model()
    user = User.objects.create_user(username=login, password=senha, email=email)
    user.groups.add(grupo_com_permissao_notificar)
    user.save()
    return user


@pytest.fixture
def membro_associacao_presidente_associacao(associacao):
    return baker.make(
        'MembroAssociacao',
        nome='Arthur Nobrega Silva',
        associacao=associacao,
        cargo_associacao=MembroEnum.PRESIDENTE_DIRETORIA_EXECUTIVA.name,
        cargo_educacao='Coordenador',
        representacao=RepresentacaoCargo.SERVIDOR.value,
        codigo_identificacao='7219999',
        email='ollyverottoboni@gmail.com',
    )


@pytest.fixture
def membro_associacao_vice_presidente_associacao(associacao):
    return baker.make(
        'MembroAssociacao',
        nome='Arthur Nobrega Junior',
        associacao=associacao,
        cargo_associacao=MembroEnum.VICE_PRESIDENTE_DIRETORIA_EXECUTIVA.name,
        cargo_educacao='Coordenador',
        representacao=RepresentacaoCargo.SERVIDOR.value,
        codigo_identificacao='7210418',
        email='ollyverottoboni@gmail.com',
    )


@pytest.fixture
def comentario_analise_prestacao(prestacao_conta_2020_1_conciliada):
    return baker.make(
        'ComentarioAnalisePrestacao',
        prestacao_conta=prestacao_conta_2020_1_conciliada,
        ordem=1,
        comentario='Teste',
    )


def test_notificar(jwt_authenticated_client_a,
                   associacao,
                   periodo_2020_1,
                   comentario_analise_prestacao,
                   usuario_presidente,
                   usuario_vice_presidente,
                   usuario_apenas_com_permissao):
    assert Notificacao.objects.count() == 0

    payload = {
        'associacao': str(associacao.uuid),
        'periodo': str(periodo_2020_1.uuid),
        'comentarios': [
            str(comentario_analise_prestacao.uuid),
        ],
        'enviar_email': False
    }

    response = jwt_authenticated_client_a.post(
        f'/api/notificacoes/notificar/', data=json.dumps(payload), content_type='application/json')

    result = json.loads(response.content)
    assert result == {"mensagem": "Processo de notificação enviado com sucesso."}
    assert Notificacao.objects.count() == 2
    assert Notificacao.objects.filter(
        usuario__username=usuario_presidente.username).first()
    assert Notificacao.objects.filter(
        usuario__username=usuario_vice_presidente.username).first()
    assert not Notificacao.objects.filter(
        usuario__username=usuario_apenas_com_permissao.username).first()

