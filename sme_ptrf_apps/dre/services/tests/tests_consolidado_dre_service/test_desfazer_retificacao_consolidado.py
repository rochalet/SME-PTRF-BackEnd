
import pytest

from sme_ptrf_apps.core.models import PrestacaoConta
from sme_ptrf_apps.dre.models import ConsolidadoDRE
from sme_ptrf_apps.dre.services.consolidado_dre_service import desfazer_retificacao_dre

pytestmark = pytest.mark.django_db


def test_desfazer_retificacao_sem_motivo_deve_levantar_excecao(
    retificacao_dre,
    prestacao_conta_pc1
):

    with pytest.raises(Exception) as excinfo:
        desfazer_retificacao_dre(
            retificacao=retificacao_dre,
            prestacoes_de_conta_a_desfazer_retificacao=[prestacao_conta_pc1.uuid],
            motivo="",
            deve_apagar_retificacao=False
        )
    assert 'É necessário informar o motivo da retificação' in str(excinfo.value)


def test_desfazer_retificacao_sem_pcs_deve_levantar_excecao(
    retificacao_dre,
    prestacao_conta_pc1
):
    with pytest.raises(Exception) as excinfo:
        desfazer_retificacao_dre(
            retificacao=retificacao_dre,
            prestacoes_de_conta_a_desfazer_retificacao=[],
            motivo="Teste",
            deve_apagar_retificacao=False
        )
    assert 'Nenhuma prestação de conta selecionada para desfazer retificação.' in str(excinfo.value)


def test_desfazer_retificacao_sem_flag_deve_apagar_retificacao_deve_levantar_excecao(
    retificacao_dre,
    prestacao_conta_pc1
):
    with pytest.raises(Exception) as excinfo:
        desfazer_retificacao_dre(
            retificacao=retificacao_dre,
            prestacoes_de_conta_a_desfazer_retificacao=[prestacao_conta_pc1.uuid],
            motivo="Teste",
            deve_apagar_retificacao=None
        )
    assert 'É necessário informar se deve apagar a retificação.' in str(excinfo.value)


def test_desfazer_retificacao_com_flag_deve_apagar_retificacao_nao_sendo_boolean_deve_levantar_excecao(
    retificacao_dre,
    prestacao_conta_pc1
):
    with pytest.raises(Exception) as excinfo:
        desfazer_retificacao_dre(
            retificacao=retificacao_dre,
            prestacoes_de_conta_a_desfazer_retificacao=[prestacao_conta_pc1.uuid],
            motivo="Teste",
            deve_apagar_retificacao="teste"
        )
    assert 'Deve apagar retificacao deve ser True ou False' in str(excinfo.value)


def test_desfazer_retificacao(
    jwt_authenticated_client_dre,
    retificacao_dre,
    prestacao_conta_pc2
):
    consolidado_original = retificacao_dre.consolidado_retificado

    assert consolidado_original.prestacoes_de_conta_do_consolidado_dre.all().count() == 0
    assert retificacao_dre.prestacoes_de_conta_do_consolidado_dre.all().count() == 1

    desfazer_retificacao_dre(
        retificacao=retificacao_dre,
        prestacoes_de_conta_a_desfazer_retificacao=[prestacao_conta_pc2.uuid],
        motivo="Teste",
        deve_apagar_retificacao=False
    )

    retificacao_dre.refresh_from_db()

    # PC foi retirada da retificacao
    assert retificacao_dre.prestacoes_de_conta_do_consolidado_dre.all().count() == 0
    assert retificacao_dre.motivo_retificacao == "Teste"

    # PC foi inserida no consolidado original
    assert consolidado_original.prestacoes_de_conta_do_consolidado_dre.all().count() == 1
    assert consolidado_original.prestacoes_de_conta_do_consolidado_dre.first() == prestacao_conta_pc2

    prestacao_conta_pc2.refresh_from_db()
    assert prestacao_conta_pc2.consolidado_dre == consolidado_original
    assert prestacao_conta_pc2.publicada is True
    assert prestacao_conta_pc2.status == PrestacaoConta.STATUS_APROVADA


def test_desfazer_retificacao_deve_apagar_retificacao(
    jwt_authenticated_client_dre,
    retificacao_dre,
    prestacao_conta_pc2
):
    consolidado_original = retificacao_dre.consolidado_retificado
    retificacao_dre_uuid = f"{retificacao_dre.uuid}"

    assert consolidado_original.prestacoes_de_conta_do_consolidado_dre.all().count() == 0
    assert retificacao_dre.prestacoes_de_conta_do_consolidado_dre.all().count() == 1

    desfazer_retificacao_dre(
        retificacao=retificacao_dre,
        prestacoes_de_conta_a_desfazer_retificacao=[prestacao_conta_pc2.uuid],
        motivo="Teste",
        deve_apagar_retificacao=True
    )


    with pytest.raises(Exception) as excinfo:
        retificacao_excluida = ConsolidadoDRE.by_uuid(retificacao_dre_uuid)

    assert 'ConsolidadoDRE matching query does not exist.' == str(excinfo.value)


    # PC foi inserida no consolidado original
    assert consolidado_original.prestacoes_de_conta_do_consolidado_dre.all().count() == 1
    assert consolidado_original.prestacoes_de_conta_do_consolidado_dre.first() == prestacao_conta_pc2

    prestacao_conta_pc2.refresh_from_db()
    assert prestacao_conta_pc2.consolidado_dre == consolidado_original
    assert prestacao_conta_pc2.publicada is True
    assert prestacao_conta_pc2.status == PrestacaoConta.STATUS_APROVADA