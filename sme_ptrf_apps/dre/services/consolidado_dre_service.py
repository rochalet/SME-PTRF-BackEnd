import logging
from django.db.models import Q, Max, Value
from django.db.models.functions import Coalesce

from ..api.serializers.ata_parecer_tecnico_serializer import AtaParecerTecnicoLookUpSerializer
from ..models import ConsolidadoDRE, AtaParecerTecnico, RelatorioConsolidadoDRE
from ..tasks import concluir_consolidado_dre_async, \
    gerar_previa_consolidado_dre_async, \
    concluir_consolidado_de_publicacoes_parciais_async

from ...core.models import Unidade, PrestacaoConta, Periodo, Associacao

logger = logging.getLogger(__name__)


def criar_ata_e_atribuir_ao_consolidado_dre(dre=None, periodo=None, consolidado_dre=None, sequencia_de_publicacao=None):
    sequencia_de_publicacao_atual = sequencia_de_publicacao['sequencia_de_publicacao_atual']
    ata = AtaParecerTecnico.criar_ou_retornar_ata_sem_consolidado_dre(dre=dre, periodo=periodo,
                                                                      sequencia_de_publicacao=sequencia_de_publicacao_atual)

    if consolidado_dre:
        ata.consolidado_dre = consolidado_dre
        ata.sequencia_de_publicacao = consolidado_dre.sequencia_de_publicacao
        ata.save(update_fields=['consolidado_dre', 'sequencia_de_publicacao'])

    return ata


def retornar_ja_publicadas(dre, periodo):
    consolidados_dre = ConsolidadoDRE.objects.filter(dre=dre, periodo=periodo, versao='FINAL')

    publicacoes_anteriores = []
    for consolidado_dre in consolidados_dre:

        tipo_publicacao = "Parcial" if consolidado_dre.eh_parcial else "Única"
        sequencia = consolidado_dre.sequencia_de_publicacao

        if tipo_publicacao == 'Parcial':
            nome_publicacao = f'Publicação {tipo_publicacao} #{sequencia}'
        else:
            nome_publicacao = 'Publicação Única'

        consolidado = {
            'titulo_relatorio': nome_publicacao,
            'sequencia': sequencia,
            'ja_publicado': True,
            'dre_nome': dre.nome,
            'uuid': consolidado_dre.uuid,
            'dre_uuid': dre.uuid,
            'periodo_uuid': periodo.uuid,
            'eh_consolidado_de_publicacoes_parciais': False,
        }

        atas_de_parecer_tecnico = consolidado_dre.atas_de_parecer_tecnico_do_consolidado_dre.all()
        ata_de_parecer_tecnico_dict = {}

        # Atas
        for ata in atas_de_parecer_tecnico:
            _ata = {
                'uuid': ata.uuid,
                'alterado_em': ata.alterado_em,
                'arquivo_pdf': ata.arquivo_pdf.path if ata.arquivo_pdf and ata.arquivo_pdf.path else None,
            }

            ata_de_parecer_tecnico_dict = _ata

        consolidado['ata_de_parecer_tecnico'] = ata_de_parecer_tecnico_dict

        # Relatorios Consolidados
        relatorios_fisico_financeiros = consolidado_dre.relatorios_consolidados_dre_do_consolidado_dre.all()
        relatorios_fisico_financeiros_list = []

        for relatorio in relatorios_fisico_financeiros:
            _relatorio = {
                'uuid': relatorio.uuid,
                'versao': relatorio.versao,
                'tipo_conta': relatorio.tipo_conta.nome if relatorio.tipo_conta and relatorio.tipo_conta.nome else "",
                'tipo_conta_uuid': relatorio.tipo_conta.uuid if relatorio.tipo_conta and relatorio.tipo_conta.uuid else "",
                'status_geracao': relatorio.status,
                'status_geracao_arquivo': relatorio.__str__(),
            }

            relatorios_fisico_financeiros_list.append(_relatorio)

        consolidado['relatorios_fisico_financeiros'] = relatorios_fisico_financeiros_list

        # Atas
        laudas = consolidado_dre.laudas_do_consolidado_dre.all()
        laudas_list = []

        for lauda in laudas:
            _lauda = {
                'uuid': lauda.uuid,
                'status': lauda.status,
                'tipo_conta': lauda.tipo_conta.nome if lauda.tipo_conta and lauda.tipo_conta.nome else "",
                'tipo_conta_uuid': lauda.tipo_conta.uuid if lauda.tipo_conta and lauda.tipo_conta.uuid else "",
                'status_geracao_arquivo': lauda.__str__(),
            }

            laudas_list.append(_lauda)

        consolidado['laudas'] = laudas_list

        publicacoes_anteriores.append(consolidado)

    return publicacoes_anteriores


def retornar_proxima_publicacao(dre, periodo, sequencia_de_publicacao, sequencia_de_publicacao_atual):
    ata_de_parecer_tecnico = AtaParecerTecnico.objects.filter(dre=dre, periodo=periodo,
                                                              sequencia_de_publicacao=sequencia_de_publicacao_atual).last()

    consolidado_dre_proxima_publicacao = ConsolidadoDRE.objects.filter(dre=dre, periodo=periodo,
                                                                       sequencia_de_publicacao=sequencia_de_publicacao_atual).last()
    relatorios_fisico_financeiros_proxima_publicacao_list = []
    uuid_consolidado_dre_proxima_publicacao = None
    if consolidado_dre_proxima_publicacao:

        uuid_consolidado_dre_proxima_publicacao = consolidado_dre_proxima_publicacao.uuid

        relatorios_fisico_financeiros_proxima_publicacao = consolidado_dre_proxima_publicacao.relatorios_consolidados_dre_do_consolidado_dre.all()

        for relatorio in relatorios_fisico_financeiros_proxima_publicacao:
            _relatorio = {
                'uuid': relatorio.uuid,
                'versao': relatorio.versao,
                'tipo_conta': relatorio.tipo_conta.nome if relatorio.tipo_conta and relatorio.tipo_conta.nome else "",
                'tipo_conta_uuid': relatorio.tipo_conta.uuid if relatorio.tipo_conta and relatorio.tipo_conta.uuid else "",
                'status_geracao': relatorio.status,
                'status_geracao_arquivo': relatorio.__str__(),
            }

            relatorios_fisico_financeiros_proxima_publicacao_list.append(_relatorio)

    if sequencia_de_publicacao['parcial']:
        titulo_relatorio = f'Publicação Parcial #{sequencia_de_publicacao_atual}'
    else:
        titulo_relatorio = 'Publicação Única'

    proxima_publicacao = {
        'titulo_relatorio': titulo_relatorio,
        'sequencia': sequencia_de_publicacao_atual,
        'ja_publicado': False,
        'dre_nome': dre.nome,
        'relatorios_fisico_financeiros': relatorios_fisico_financeiros_proxima_publicacao_list,
        'ata_de_parecer_tecnico': AtaParecerTecnicoLookUpSerializer(ata_de_parecer_tecnico,
                                                                    many=False).data if ata_de_parecer_tecnico else {},
        'laudas': [],
        'dre_uuid': dre.uuid,
        'periodo_uuid': periodo.uuid,
        'uuid': uuid_consolidado_dre_proxima_publicacao,
        'eh_consolidado_de_publicacoes_parciais': False,
    }

    return proxima_publicacao


def retornar_consolidado_de_publicacoes_parciais(dre, periodo, sequencia_de_publicacao_atual):
    relatorios_fisico_financeiros_consolidado_de_publicacoes_parciais = RelatorioConsolidadoDRE.objects.filter(
        dre=dre,
        periodo=periodo,
        consolidado_dre__isnull=True,
        versao='CONSOLIDADA'
    )

    relatorios_fisico_financeiros_consolidado_de_publicacoes_parciais_list = []

    for relatorio in relatorios_fisico_financeiros_consolidado_de_publicacoes_parciais:
        _relatorio = {
            'uuid': relatorio.uuid,
            'versao': relatorio.versao,
            'tipo_conta': relatorio.tipo_conta.nome if relatorio.tipo_conta and relatorio.tipo_conta.nome else "",
            'tipo_conta_uuid': relatorio.tipo_conta.uuid if relatorio.tipo_conta and relatorio.tipo_conta.uuid else "",
            'status_geracao': relatorio.status,
            'status_geracao_arquivo': relatorio.__str__(),
        }

        relatorios_fisico_financeiros_consolidado_de_publicacoes_parciais_list.append(_relatorio)

    proxima_publicacao_consolidado_de_publicacoes_parciais = {
        'titulo_relatorio': "Relatório Consolidado",
        'sequencia': sequencia_de_publicacao_atual,
        'ja_publicado': False,
        'dre_nome': dre.nome,
        'relatorios_fisico_financeiros': relatorios_fisico_financeiros_consolidado_de_publicacoes_parciais_list,
        'ata_de_parecer_tecnico': {},
        'laudas': [],
        'dre_uuid': dre.uuid,
        'periodo_uuid': periodo.uuid,
        'uuid': None,
        'eh_consolidado_de_publicacoes_parciais': True,
    }

    return proxima_publicacao_consolidado_de_publicacoes_parciais


def retornar_consolidados_dre_ja_criados_e_proxima_criacao(dre=None, periodo=None):
    dre_uuid = dre.uuid
    periodo_uuid = periodo.uuid

    sequencia_de_publicacao = verificar_se_status_parcial_ou_total_e_retornar_sequencia_de_publicacao(dre_uuid,
                                                                                                      periodo_uuid)

    sequencia_de_publicacao_atual = sequencia_de_publicacao['sequencia_de_publicacao_atual']

    publicacoes_anteriores = retornar_ja_publicadas(dre, periodo)

    quantidade_ues_cnpj = Associacao.objects.filter(unidade__dre=dre).exclude(cnpj__exact='').count()
    # quantidade_ues_cnpj = 2
    quantidade_pcs_publicadas = PrestacaoConta.objects.filter(periodo__uuid=periodo_uuid,
                                                              associacao__unidade__dre__uuid=dre_uuid,
                                                              publicada=True).count()
    quantidade_consolidados_dre_publicados = ConsolidadoDRE.objects.filter(
        dre=dre,
        periodo=periodo,
        versao="FINAL",
        sequencia_de_publicacao__gt=0,
        eh_parcial=True
    ).count()

    consolidado_de_publicacoes_parciais = (quantidade_pcs_publicadas == quantidade_ues_cnpj) and quantidade_consolidados_dre_publicados > 0

    if consolidado_de_publicacoes_parciais:
        proxima_publicacao = retornar_consolidado_de_publicacoes_parciais(
            dre,
            periodo,
            sequencia_de_publicacao_atual
        )
    else:
        proxima_publicacao = retornar_proxima_publicacao(
            dre,
            periodo,
            sequencia_de_publicacao,
            sequencia_de_publicacao_atual
        )

    result = {
        'proxima_publicacao': proxima_publicacao,
        'publicacoes_anteriores': publicacoes_anteriores,
    }

    return result


def retornar_trilha_de_status(dre_uuid=None, periodo_uuid=None, add_aprovado_ressalva=False,
                              add_info_devolvidas_retornadas=False):
    """
    :param add_aprovado_ressalva: True para retornar a quantidade de aprovados com ressalva separadamente ou
    False para retornar a quantidade de aprovadas com ressalva somada a quantidade de aprovadas

    :param add_info_devolvidas_retornadas: True para retornar a quantidade de devolvidas retornadas no card de
    devolução.
    """

    """
    Destaque ou não destaque do status
        0 - Simples: Circulo preenchido verde
        1 - Duplo: Circulo preenchido verde e borda verde
        2 - Vermelho: Circulo preenchido vermelho
    """

    from ...core.models import Associacao, PrestacaoConta

    titulo_e_estilo_css = {
        'NAO_RECEBIDA':
            {
                'titulo': 'Não recebidas',
                'estilo_css': 2
            },
        'RECEBIDA':
            {
                'titulo': 'Recebidas e<br/>aguardando análise',
                'estilo_css': 0
            },
        'DEVOLVIDA':
            {
                'titulo': 'Devolvidas <br/>para acertos',
                'estilo_css': 0
            },
        'EM_ANALISE':
            {
                'titulo': 'Em análise',
                'estilo_css': 0
            },
        'CONCLUIDO':
            {
                'titulo': 'Concluídas <br/>Documentos não gerados',
                'estilo_css': 1
            },
        'PUBLICADO':
            {
                'titulo': 'Concluídas <br/>Documentos gerados',
                'estilo_css': 0
            },
        'APROVADA':
            {
                'titulo': 'Aprovadas',
                'estilo_css': 0
            },
        'REPROVADA':
            {
                'titulo': 'Reprovadas',
                'estilo_css': 0
            },

    }

    if add_aprovado_ressalva:
        titulo_e_estilo_css['APROVADA_RESSALVA']['titulo'] = "Aprovadas com ressalvas"
        titulo_e_estilo_css['APROVADA_RESSALVA']['estilo_css'] = 1

    cards = []
    qs = PrestacaoConta.objects.filter(periodo__uuid=periodo_uuid, associacao__unidade__dre__uuid=dre_uuid)

    quantidade_pcs_apresentadas = 0
    for status, itens in titulo_e_estilo_css.items():
        if status == 'NAO_RECEBIDA':
            continue

        quantidade_status = qs.filter(status=status).count()

        if status == 'APROVADA' and not add_aprovado_ressalva:
            quantidade_status += qs.filter(status='APROVADA_RESSALVA').count()

        if status == 'DEVOLVIDA':
            quantidade_status += qs.filter(status__in=['DEVOLVIDA_RETORNADA', 'DEVOLVIDA_RECEBIDA']).count()

        quantidade_pcs_apresentadas += quantidade_status

        if status == 'DEVOLVIDA' and add_info_devolvidas_retornadas:
            quantidade_retornadas = qs.filter(status='DEVOLVIDA_RETORNADA').count()
            card = {
                "titulo": itens['titulo'],
                "estilo_css": itens['estilo_css'],
                "quantidade_prestacoes": quantidade_status,
                "quantidade_retornadas": quantidade_retornadas,
                "status": status
            }
            cards.append(card)
        elif not status == 'PUBLICADO' and not status == 'CONCLUIDO':
            card = {
                "titulo": itens['titulo'],
                "estilo_css": itens['estilo_css'],
                "quantidade_prestacoes": quantidade_status,
                "status": status
            }
            cards.append(card)

        if status == 'PUBLICADO':
            quantidade_pcs_publicadas = qs.filter(publicada=True).count()
            card_publicadas = {
                "titulo": itens['titulo'],
                "estilo_css": itens['estilo_css'],
                "quantidade_prestacoes": quantidade_pcs_publicadas,
                "status": 'PUBLICADO'
            }
            cards.append(card_publicadas)

        if status == 'CONCLUIDO':
            quantidade_pcs_concluidas = qs.filter(
                (Q(status='APROVADA') | Q(status='APROVADA_RESSALVA') | Q(status='REPROVADA')) &
                Q(publicada=False)
            ).count()
            card_concluidas = {
                "titulo": itens['titulo'],
                "estilo_css": itens['estilo_css'],
                "quantidade_prestacoes": quantidade_pcs_concluidas,
                "status": 'CONCLUIDO'
            }
            cards.append(card_concluidas)

    quantidade_unidades_dre = Associacao.objects.filter(unidade__dre__uuid=dre_uuid).exclude(cnpj__exact='').count()
    quantidade_pcs_nao_apresentadas = quantidade_unidades_dre - quantidade_pcs_apresentadas
    card_nao_recebidas = {
        "titulo": titulo_e_estilo_css['NAO_RECEBIDA']['titulo'],
        "estilo_css": titulo_e_estilo_css['NAO_RECEBIDA']['estilo_css'],
        "quantidade_prestacoes": quantidade_pcs_nao_apresentadas,
        "quantidade_nao_recebida": qs.filter(status='NAO_RECEBIDA').count(),
        "status": 'NAO_RECEBIDA'
    }

    cards.insert(0, card_nao_recebidas)

    return cards


def status_consolidado_dre(dre, periodo):
    """
    Calcula o status Consolidado da DRE em determinado período:

    PCs em análise?	Relatório gerado?	Texto status	                                                                            Cor
    Sim	            Não	                Ainda constam prestações de contas das associações em análise. Relatório não gerado.	    0
    Sim	            Sim (parcial)	    Ainda constam prestações de contas das associações em análise. Relatório parcial gerado.	1
    Não	            Não	                Análise de prestações de contas das associações completa. Relatório não gerado.	            2
    Não	            Sim (parcial)	    Análise de prestações de contas das associações completa. Relatório parcial gerado.	        2
    Não	            Sim (final)	        Análise de prestações de contas das associações completa. Relatório final gerado.	        3
    """

    LEGENDA_COR = {
        'NAO_GERADOS': {'com_pcs_em_analise': 0, 'sem_pcs_em_analise': 2},
        'GERADOS_PARCIAIS': {'com_pcs_em_analise': 1, 'sem_pcs_em_analise': 2},
        'GERADOS_TOTAIS': {'com_pcs_em_analise': 0, 'sem_pcs_em_analise': 3},
        'EM_PROCESSAMENTO': {'com_pcs_em_analise': 0, 'sem_pcs_em_analise': 3},
    }

    pcs_em_analise = PrestacaoConta.objects.filter(periodo=periodo,
                                                   status__in=['EM_ANALISE', 'RECEBIDA', 'NAO_RECEBIDA', 'DEVOLVIDA'],
                                                   associacao__unidade__dre=dre).exists()

    consolidados_dre = ConsolidadoDRE.objects.filter(dre=dre, periodo=periodo)

    status_list = []

    if consolidados_dre:
        for consolidado_dre in consolidados_dre:

            status_consolidado_dre = consolidado_dre.status if consolidado_dre else 'NAO_GERADOS'

            status_txt_consolidado_dre = f'{ConsolidadoDRE.STATUS_NOMES[status_consolidado_dre]}.'

            if pcs_em_analise:
                status_txt_analise = 'Ainda constam prestações de contas das associações em análise.'
            else:
                status_txt_analise = 'Análise de prestações de contas das associações completa.'

            status_txt_geracao = f'{status_txt_analise} {status_txt_consolidado_dre}'

            cor_idx = LEGENDA_COR[status_consolidado_dre][
                'com_pcs_em_analise' if pcs_em_analise else 'sem_pcs_em_analise']

            status = {
                'pcs_em_analise': pcs_em_analise,
                'status_geracao': status_consolidado_dre,
                'status_txt': status_txt_geracao,
                'cor_idx': cor_idx,
                'status_arquivo': 'Documento pendente de geração' if status_consolidado_dre == 'NAO_GERADO' else consolidado_dre.__str__(),
                'consolidado_dre_uuid': consolidado_dre.uuid,
            }

            status_list.append(status)
    else:
        status_consolidado_dre = 'NAO_GERADOS'

        status_txt_consolidado_dre = f'{ConsolidadoDRE.STATUS_NOMES[status_consolidado_dre]}.'

        if pcs_em_analise:
            status_txt_analise = 'Ainda constam prestações de contas das associações em análise.'
        else:
            status_txt_analise = 'Análise de prestações de contas das associações completa.'

        cor_idx = LEGENDA_COR[status_consolidado_dre]['com_pcs_em_analise' if pcs_em_analise else 'sem_pcs_em_analise']

        status_txt_geracao = f'{status_txt_analise} {status_txt_consolidado_dre}'

        status = {
            'pcs_em_analise': pcs_em_analise,
            'status_txt': status_txt_geracao,
            'status_geracao': status_consolidado_dre,
            'cor_idx': cor_idx,
        }

        status_list.append(status)

    return status_list


def verificar_se_status_parcial_ou_total_e_retornar_sequencia_de_publicacao(dre_uuid, periodo_uuid):
    dre = Unidade.dres.get(uuid=dre_uuid)
    periodo = Periodo.by_uuid(periodo_uuid)

    results = retornar_trilha_de_status(dre_uuid, periodo_uuid)

    total_associacoes_dre = Associacao.objects.filter(unidade__dre__uuid=dre_uuid).exclude(cnpj__exact='').count()
    # total_associacoes_dre = 2
    total_concluido = [d['quantidade_prestacoes'] for d in results if d['status'] == "CONCLUIDO"][0]

    eh_parcial = total_concluido < total_associacoes_dre

    sequencia_de_publicacao_atual = ConsolidadoDRE.objects.filter(
        dre=dre,
        periodo=periodo
    ).aggregate(max_sequencia_de_publicacao=Coalesce(Max('sequencia_de_publicacao'), Value(0)))[
        'max_sequencia_de_publicacao']

    ultimo_consolidado_criado = ConsolidadoDRE.objects.filter(dre=dre, periodo=periodo,
                                                              sequencia_de_publicacao=sequencia_de_publicacao_atual).last()
    versao_ultimo_consolidado_criado_for_publicado = True if ultimo_consolidado_criado and ultimo_consolidado_criado.versao == 'FINAL' else False

    if not eh_parcial:
        sequencia_de_publicacao_atual = 0
    elif sequencia_de_publicacao_atual == 0 or not sequencia_de_publicacao_atual:
        sequencia_de_publicacao_atual = 1
    elif versao_ultimo_consolidado_criado_for_publicado:
        sequencia_de_publicacao_atual = sequencia_de_publicacao_atual + 1

    obj_parcial = {
        "parcial": eh_parcial,
        "sequencia_de_publicacao_atual": sequencia_de_publicacao_atual,
    }

    return obj_parcial


def gerar_previa_consolidado_dre(dre, periodo, parcial, usuario):
    eh_parcial = parcial['parcial']
    sequencia_de_publicacao = parcial['sequencia_de_publicacao_atual']
    consolidado_dre = ConsolidadoDRE.criar_ou_retornar_consolidado_dre(dre=dre, periodo=periodo,
                                                                       sequencia_de_publicacao=sequencia_de_publicacao)
    logger.info(f'Criado Pŕevia do Consolidado DRE  {consolidado_dre}.')

    consolidado_dre.passar_para_status_em_processamento()
    logger.info(f'Consolidado DRE em processamento - {consolidado_dre}.')

    consolidado_dre.atribuir_versao(previa=True)
    consolidado_dre.atribuir_se_eh_parcial(parcial=eh_parcial)

    ata_parecer_tecnico = AtaParecerTecnico.objects.filter(
        dre=dre,
        periodo=periodo,
        sequencia_de_publicacao=sequencia_de_publicacao
    ).last()

    if ata_parecer_tecnico:
        ata_parecer_tecnico.consolidado_dre = consolidado_dre
        ata_parecer_tecnico.sequencia_de_publicacao = consolidado_dre.sequencia_de_publicacao
        ata_parecer_tecnico.save(update_fields=['consolidado_dre', 'sequencia_de_publicacao'])

    dre_uuid = dre.uuid
    periodo_uuid = periodo.uuid
    consolidado_dre_uuid = consolidado_dre.uuid

    gerar_previa_consolidado_dre_async.delay(
        dre_uuid=dre_uuid,
        periodo_uuid=periodo_uuid,
        parcial=parcial,
        usuario=usuario,
        consolidado_dre_uuid=consolidado_dre_uuid,
        sequencia_de_publicacao=sequencia_de_publicacao,
        apenas_nao_publicadas=True,
    )

    return consolidado_dre


def concluir_consolidado_dre(dre, periodo, parcial, usuario):
    eh_parcial = parcial['parcial']
    sequencia_de_publicacao = parcial['sequencia_de_publicacao_atual']

    if eh_parcial:
        logger.info('Apagando qualquer prévia existente de um consolidado único para a DRE no período...')
        ConsolidadoDRE.objects.filter(
            dre=dre,
            periodo=periodo,
            sequencia_de_publicacao=0,
            versao=ConsolidadoDRE.VERSAO_PREVIA,
        ).delete()
    else:
        logger.info('Apagando qualquer prévia existente de um consolidado parcial para a DRE no período...')
        ConsolidadoDRE.objects.filter(
            dre=dre,
            periodo=periodo,
            sequencia_de_publicacao__gt=0,
            versao=ConsolidadoDRE.VERSAO_PREVIA,
        ).delete()

    consolidado_dre = ConsolidadoDRE.criar_ou_retornar_consolidado_dre(dre=dre, periodo=periodo,
                                                                       sequencia_de_publicacao=sequencia_de_publicacao)
    logger.info(f'Criado Consolidado DRE  {consolidado_dre}.')

    consolidado_dre.passar_para_status_em_processamento()
    logger.info(f'Consolidado DRE em processamento - {consolidado_dre}.')

    consolidado_dre.atribuir_versao(previa=False)
    consolidado_dre.atribuir_se_eh_parcial(parcial=eh_parcial)

    ata_parecer_tecnico = AtaParecerTecnico.criar_ou_retornar_ata_sem_consolidado_dre(dre, periodo,
                                                                                      sequencia_de_publicacao)

    dre_uuid = dre.uuid
    periodo_uuid = periodo.uuid
    consolidado_dre_uuid = consolidado_dre.uuid
    ata_parecer_tecnico_uuid = ata_parecer_tecnico.uuid

    ata_parecer_tecnico.consolidado_dre = consolidado_dre
    ata_parecer_tecnico.sequencia_de_publicacao = consolidado_dre.sequencia_de_publicacao
    ata_parecer_tecnico.save(update_fields=['consolidado_dre', 'sequencia_de_publicacao'])

    concluir_consolidado_dre_async.delay(
        dre_uuid=dre_uuid,
        periodo_uuid=periodo_uuid,
        parcial=parcial,
        usuario=usuario,
        consolidado_dre_uuid=consolidado_dre_uuid,
        ata_uuid=ata_parecer_tecnico_uuid,
        sequencia_de_publicacao=sequencia_de_publicacao,
        apenas_nao_publicadas=True,
    )

    return consolidado_dre


def concluir_consolidado_de_publicacoes_parciais(dre, periodo, usuario):
    logger.info(f'Iniciando a criação do Consolidado de publicacoes parciais')

    dre_uuid = dre.uuid
    periodo_uuid = periodo.uuid

    concluir_consolidado_de_publicacoes_parciais_async.delay(
        dre_uuid=dre_uuid,
        periodo_uuid=periodo_uuid,
        usuario=usuario,
    )
