import logging

from rest_framework import serializers

from ...api.serializers import AssociacaoInfoAtaSerializer
from ...api.serializers.periodo_serializer import PeriodoLookUpSerializer
from ...api.serializers.presentes_ata_serializer import PresentesAtaSerializer, PresentesAtaCreateSerializer
from ...models import Ata, PrestacaoConta
from sme_ptrf_apps.utils.update_instance_from_dict import update_instance_from_dict


class AtaLookUpSerializer(serializers.ModelSerializer):
    nome = serializers.SerializerMethodField('get_nome_ata')
    alterado_em = serializers.SerializerMethodField('get_alterado_em')

    def get_nome_ata(self, obj):
        return obj.nome

    def get_alterado_em(self, obj):
        return obj.preenchida_em

    class Meta:
        model = Ata
        fields = ('uuid', 'nome', 'alterado_em', "completa")


class AtaSerializer(serializers.ModelSerializer):
    nome = serializers.SerializerMethodField('get_nome_ata')
    hora_reuniao = serializers.SerializerMethodField('get_hora_reuniao')
    associacao = AssociacaoInfoAtaSerializer(many=False)
    periodo = PeriodoLookUpSerializer(many=False)
    prestacao_conta = serializers.SlugRelatedField(
        slug_field='uuid',
        required=False,
        queryset=PrestacaoConta.objects.all()
    )

    presentes_na_ata = PresentesAtaSerializer(many=True)

    def get_nome_ata(self, obj):
        return obj.nome

    def get_hora_reuniao(self, obj):
        return obj.hora_reuniao.strftime('%H:%M')

    class Meta:
        model = Ata
        fields = (
            'uuid',
            'arquivo_pdf',
            'status_geracao_pdf',
            'prestacao_conta',
            'nome',
            'periodo',
            'associacao',
            'tipo_ata',
            'tipo_reuniao',
            'convocacao',
            'data_reuniao',
            'local_reuniao',
            'presidente_reuniao',
            'cargo_presidente_reuniao',
            'secretario_reuniao',
            'cargo_secretaria_reuniao',
            'comentarios',
            'parecer_conselho',
            'retificacoes',
            'presentes_na_ata',
            'hora_reuniao',
            'justificativa_repasses_pendentes',
        )


class AtaCreateSerializer(serializers.ModelSerializer):
    nome = serializers.SerializerMethodField('get_nome_ata')
    associacao = AssociacaoInfoAtaSerializer(many=False)
    periodo = PeriodoLookUpSerializer(many=False)
    prestacao_conta = serializers.SlugRelatedField(
        slug_field='uuid',
        required=False,
        queryset=PrestacaoConta.objects.all()
    )

    presentes_na_ata = PresentesAtaCreateSerializer(many=True, required=False)

    def get_nome_ata(self, obj):
        return obj.nome

    def create(self, validated_data):
        presentes_na_ata = validated_data.pop('presentes_na_ata')
        ata = Ata.objects.create(**validated_data)

        presentes_lista = []
        for presente in presentes_na_ata:
            presentes_object = PresentesAtaCreateSerializer().create(presente)
            presentes_object.eh_conselho_fiscal()
            presentes_lista.append(presentes_object)

        ata.presentes_na_ata.set(presentes_lista)
        ata.save()

        return ata

    def update(self, instance, validated_data):
        presentes_json = validated_data.pop('presentes_na_ata')
        instance.presentes_na_ata.all().delete()
        presentes_lista = []
        for presente in presentes_json:
            presente_object = PresentesAtaCreateSerializer().create(presente)
            presente_object.eh_conselho_fiscal()
            presentes_lista.append(presente_object)

        update_instance_from_dict(instance, validated_data)
        instance.presentes_na_ata.set(presentes_lista)
        instance.save()

        return instance

    class Meta:
        model = Ata
        exclude = ('id',)
