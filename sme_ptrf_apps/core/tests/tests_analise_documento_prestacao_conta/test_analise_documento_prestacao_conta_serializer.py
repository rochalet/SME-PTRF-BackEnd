import pytest

from ...api.serializers import AnaliseDocumentoPrestacaoContaRetrieveSerializer

pytestmark = pytest.mark.django_db


def test_retrieve_serializer(analise_documento_prestacao_conta_2020_1_ata_correta):
    serializer = AnaliseDocumentoPrestacaoContaRetrieveSerializer(analise_documento_prestacao_conta_2020_1_ata_correta)
    assert serializer.data is not None
    assert serializer.data['uuid']
    assert serializer.data['id']
    assert serializer.data['resultado'] == 'CORRETO'
    assert serializer.data['conta_associacao']
    assert serializer.data['analise_prestacao_conta']
    assert serializer.data['tipo_documento_prestacao_conta']
    assert serializer.data['solicitacoes_de_ajuste_da_analise'] == []