import pytest

from sme_ptrf_apps.dre.models import RelatorioConsolidadoDRE, AtaParecerTecnico, Lauda
from sme_ptrf_apps.dre.services.vincular_consolidado_service import VincularConsolidadoService

pytestmark = pytest.mark.django_db


def test_vincular_consolidado_service_vincular_artefato_usando_consolidado_existente(
    vcs_periodo_2022_1,
    vcs_dre_ipiranga,
    vcs_consolidado_dre_ipiranga_2022_1,
    vcs_relatorio_dre_consolidado_gerado_total_desvinculado
):
    VincularConsolidadoService.vincular_artefato(vcs_relatorio_dre_consolidado_gerado_total_desvinculado)

    relatorio = RelatorioConsolidadoDRE.by_id(vcs_relatorio_dre_consolidado_gerado_total_desvinculado.id)

    assert relatorio.consolidado_dre == vcs_consolidado_dre_ipiranga_2022_1


def test_vincular_consolidado_service_vincular_artefato_criando_consolidado_inexistente(
    vcs_periodo_2022_1,
    vcs_dre_ipiranga,
    vcs_relatorio_dre_consolidado_gerado_total_desvinculado
):
    from sme_ptrf_apps.dre.models import ConsolidadoDRE

    VincularConsolidadoService.vincular_artefato(vcs_relatorio_dre_consolidado_gerado_total_desvinculado)

    relatorio = RelatorioConsolidadoDRE.by_id(vcs_relatorio_dre_consolidado_gerado_total_desvinculado.id)

    assert relatorio.consolidado_dre is not None

    assert relatorio.consolidado_dre.periodo == vcs_periodo_2022_1
    assert relatorio.consolidado_dre.dre == vcs_dre_ipiranga
    assert relatorio.consolidado_dre.sequencia_de_publicacao == 0
    assert relatorio.consolidado_dre.eh_parcial is False
    assert relatorio.consolidado_dre.status == ConsolidadoDRE.STATUS_GERADOS_TOTAIS


def test_vincular_consolidado_service_vincular_artefato_usando_ultima_sequencia_de_consolidados_existentes(
    vcs_periodo_2022_1,
    vcs_dre_ipiranga,
    vcs_consolidado_dre_ipiranga_2022_1_parcial_1,
    vcs_consolidado_dre_ipiranga_2022_1_parcial_2,
    vcs_relatorio_dre_consolidado_gerado_total_desvinculado
):
    VincularConsolidadoService.vincular_artefato(vcs_relatorio_dre_consolidado_gerado_total_desvinculado)

    relatorio = RelatorioConsolidadoDRE.by_id(vcs_relatorio_dre_consolidado_gerado_total_desvinculado.id)

    assert relatorio.consolidado_dre == vcs_consolidado_dre_ipiranga_2022_1_parcial_2


def test_vincular_consolidado_service_vincular_ata_gravando_ultima_sequencia_de_consolidados_existentes(
    vcs_periodo_2022_1,
    vcs_dre_ipiranga,
    vcs_consolidado_dre_ipiranga_2022_1_parcial_1,
    vcs_consolidado_dre_ipiranga_2022_1_parcial_2,
    vcs_ata_parecer_tecnico_desvinculada
):
    VincularConsolidadoService.vincular_artefato(vcs_ata_parecer_tecnico_desvinculada)

    ata = AtaParecerTecnico.by_id(vcs_ata_parecer_tecnico_desvinculada.id)

    assert ata.consolidado_dre == vcs_consolidado_dre_ipiranga_2022_1_parcial_2
    assert ata.sequencia_de_publicacao == 2


def test_vincular_consolidado_service_vincular_ata_gravando_sequencia_de_consolidado_criado(
    vcs_periodo_2022_1,
    vcs_dre_ipiranga,
    vcs_ata_parecer_tecnico_desvinculada
):
    VincularConsolidadoService.vincular_artefato(vcs_ata_parecer_tecnico_desvinculada)

    ata = AtaParecerTecnico.by_id(vcs_ata_parecer_tecnico_desvinculada.id)

    assert ata.consolidado_dre is not None
    assert ata.sequencia_de_publicacao == 0


def test_vincular_consolidado_service_vincular_artefato_lauda_usando_consolidado_existente(
    vcs_periodo_2022_1,
    vcs_dre_ipiranga,
    vcs_consolidado_dre_ipiranga_2022_1,
    vcs_lauda_desvinculada
):
    VincularConsolidadoService.vincular_artefato(vcs_lauda_desvinculada)

    relatorio = Lauda.by_id(vcs_lauda_desvinculada.id)

    assert relatorio.consolidado_dre == vcs_consolidado_dre_ipiranga_2022_1


def test_vincular_consolidado_service_vincular_artefato_lauda_criando_consolidado_inexistente(
    vcs_periodo_2022_1,
    vcs_dre_ipiranga,
    vcs_lauda_desvinculada
):
    from sme_ptrf_apps.dre.models import ConsolidadoDRE

    VincularConsolidadoService.vincular_artefato(vcs_lauda_desvinculada)

    lauda = Lauda.by_id(vcs_lauda_desvinculada.id)

    assert lauda.consolidado_dre is not None

    assert lauda.consolidado_dre.periodo == vcs_periodo_2022_1
    assert lauda.consolidado_dre.dre == vcs_dre_ipiranga
    assert lauda.consolidado_dre.eh_parcial is False
    assert lauda.consolidado_dre.status == ConsolidadoDRE.STATUS_GERADOS_TOTAIS