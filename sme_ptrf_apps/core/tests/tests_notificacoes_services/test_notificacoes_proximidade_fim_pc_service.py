import pytest

from freezegun import freeze_time

from ....core.models import Notificacao, Periodo
from ....core.services.notificacao_services import notificar_proximidade_fim_periodo_prestacao_conta

pytestmark = pytest.mark.django_db


@freeze_time("2021-06-13")
def test_deve_notificar_usuarios_5_dias_antes(
    associacao_a,
    usuario_notificavel,
    usuario_nao_notificavel,
    periodo_2020_4_pc_2021_01_01_a_2021_01_15,
    periodo_2021_1_pc_2021_04_1_a_2021_04_15,
    periodo_notifica_proximidade_fim_pc,
    parametro_proximidade_fim_pc_5_dias,
):

    assert not Notificacao.objects.exists()

    notificar_proximidade_fim_periodo_prestacao_conta(enviar_email=False)

    assert Notificacao.objects.count() == 1

    notificacao = Notificacao.objects.first()

    assert notificacao.tipo == Notificacao.TIPO_NOTIFICACAO_INFORMACAO
    assert notificacao.categoria == Notificacao.CATEGORIA_NOTIFICACAO_ELABORACAO_PC
    assert notificacao.remetente == Notificacao.REMETENTE_NOTIFICACAO_SISTEMA
    assert notificacao.titulo == f"Últimos dias para enviar a PC {periodo_notifica_proximidade_fim_pc.referencia}"
    assert notificacao.descricao == f"Faltam apenas 5 dia(s) para o término do período de prestações de contas. Envie a sua prestação de contas."
    assert notificacao.usuario == usuario_notificavel


@freeze_time("2021-06-18")
def test_deve_notificar_usuarios_no_dia(
    associacao_a,
    usuario_notificavel,
    usuario_nao_notificavel,
    periodo_2020_4_pc_2021_01_01_a_2021_01_15,
    periodo_2021_1_pc_2021_04_1_a_2021_04_15,
    periodo_notifica_proximidade_fim_pc,
    parametro_proximidade_fim_pc_5_dias,
):

    assert not Notificacao.objects.exists()

    notificar_proximidade_fim_periodo_prestacao_conta(enviar_email=False)

    assert Notificacao.objects.count() == 1


@freeze_time("2021-06-18")
def test_deve_flagar_periodo_como_notificado(
    associacao_a,
    usuario_notificavel,
    usuario_nao_notificavel,
    periodo_2020_4_pc_2021_01_01_a_2021_01_15,
    periodo_2021_1_pc_2021_04_1_a_2021_04_15,
    periodo_notifica_proximidade_fim_pc,
    parametro_proximidade_fim_pc_5_dias,
):

    assert not periodo_notifica_proximidade_fim_pc.notificacao_proximidade_fim_pc_realizada

    notificar_proximidade_fim_periodo_prestacao_conta(enviar_email=False)

    periodo = Periodo.objects.get(referencia="2021.6")
    assert periodo.notificacao_proximidade_fim_pc_realizada


@freeze_time("2021-06-18")
def test_nao_deve_re_notificar_periodo(
    associacao_a,
    usuario_notificavel,
    usuario_nao_notificavel,
    periodo_2020_4_pc_2021_01_01_a_2021_01_15,
    periodo_2021_1_pc_2021_04_1_a_2021_04_15,
    periodo_notifica_proximidade_fim_pc,
    parametro_proximidade_fim_pc_5_dias,
):
    periodo_notifica_proximidade_fim_pc.notificacao_proximidade_fim_prestacao_de_contas_realizada()

    notificar_proximidade_fim_periodo_prestacao_conta()

    assert not Notificacao.objects.exists()


