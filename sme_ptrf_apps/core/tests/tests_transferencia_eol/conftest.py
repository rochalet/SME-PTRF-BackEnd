import datetime

import pytest
from model_bakery import baker


@pytest.fixture
def transf_eol_periodo_2022_2():
    return baker.make(
        'Periodo',
        referencia='2022.2',
        data_inicio_realizacao_despesas=datetime.date(2022, 7, 1),
        data_fim_realizacao_despesas=datetime.date(2022, 12, 31),
        periodo_anterior=None
    )


@pytest.fixture
def transf_eol_tipo_conta_cheque():
    return baker.make(
        'TipoConta',
        nome='Cheque',
    )


@pytest.fixture
def transf_eol_tipo_conta_cartao():
    return baker.make(
        'TipoConta',
        nome='Cartão',
    )


@pytest.fixture
def transf_eol_acao_ptrf():
    return baker.make('Acao', nome='PTRF')


@pytest.fixture
def transf_eol_acao_role():
    return baker.make('Acao', nome='Rolê Cultural')


@pytest.fixture
def transferencia_eol(tipo_conta, transf_eol_tipo_conta_cartao):
    return baker.make(
        'TransferenciaEol',
        eol_transferido='400232',
        eol_historico='900232',
        tipo_nova_unidade='CEMEI',
        data_inicio_atividades=datetime.date(2022, 7, 1),
        tipo_conta_transferido=transf_eol_tipo_conta_cartao,
        status_processamento='PENDENTE',
        log_execucao='Teste',
    )


@pytest.fixture
def transf_eol_unidade_eol_transferido(dre):
    return baker.make(
        'Unidade',
        nome='Unidade EOL Transferido',
        tipo_unidade='CEI',
        codigo_eol='400232',
        dre=dre,
    )


@pytest.fixture
def transf_eol_unidade_eol_historico_ja_existente(dre):
    return baker.make(
        'Unidade',
        nome='Unidade Histórico',
        tipo_unidade='CEMEI',
        codigo_eol='900232',
        dre=dre,
    )


@pytest.fixture
def transf_eol_associacao_eol_transferido(transf_eol_unidade_eol_transferido):
    return baker.make(
        'Associacao',
        nome='Escola Eol Transferido',
        cnpj='52.302.275/0001-83',
        unidade=transf_eol_unidade_eol_transferido,
    )


@pytest.fixture
def transf_eol_conta_associacao_cheque(
    transf_eol_associacao_eol_transferido,
    transf_eol_tipo_conta_cheque
):
    return baker.make(
        'ContaAssociacao',
        associacao=transf_eol_associacao_eol_transferido,
        tipo_conta=transf_eol_tipo_conta_cheque,
        banco_nome='Banco do Brasil',
        agencia='12345',
        numero_conta='123456-x',
    )


@pytest.fixture
def transf_eol_conta_associacao_cartao(
    transf_eol_associacao_eol_transferido,
    transf_eol_tipo_conta_cartao
):
    return baker.make(
        'ContaAssociacao',
        associacao=transf_eol_associacao_eol_transferido,
        tipo_conta=transf_eol_tipo_conta_cartao,
        banco_nome='ITAU',
        agencia='45678',
        numero_conta='999999-x',
    )


@pytest.fixture
def transf_eol_acao_associacao_ptrf(transf_eol_associacao_eol_transferido, transf_eol_acao_ptrf):
    return baker.make(
        'AcaoAssociacao',
        associacao=transf_eol_associacao_eol_transferido,
        acao=transf_eol_acao_ptrf
    )


@pytest.fixture
def transf_eol_acao_associacao_role(transf_eol_associacao_eol_transferido, transf_eol_acao_role):
    return baker.make(
        'AcaoAssociacao',
        associacao=transf_eol_associacao_eol_transferido,
        acao=transf_eol_acao_role
    )


@pytest.fixture
def transf_eol_fechamento_periodo(
    transf_eol_periodo_2022_2,
    transf_eol_associacao_eol_transferido,
    transf_eol_conta_associacao_cheque,
    transf_eol_acao_associacao_ptrf,
):
    return baker.make(
        'FechamentoPeriodo',
        periodo=transf_eol_periodo_2022_2,
        associacao=transf_eol_associacao_eol_transferido,
        conta_associacao=transf_eol_conta_associacao_cheque,
        acao_associacao=transf_eol_acao_associacao_ptrf,
    )
