from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import exceptions
from sme_ptrf_apps.receitas.models import Receita
from sme_ptrf_apps.despesas.models import Despesa
from sme_ptrf_apps.core.models import PrestacaoConta
from sme_ptrf_apps.core.models import Associacao


class PermissaoCRUD(BasePermission):
    perms_map = {
        'GET': ['view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['add_%(model_name)s'],
        'PUT': ['change_%(model_name)s'],
        'PATCH': ['change_%(model_name)s'],
        'DELETE': ['delete_%(model_name)s'],
    }

    def get_required_permissions(self, method, model_cls):
        """
        Given a model and an HTTP method, return the list of permission
        codes that the user is required to have.
        """
        kwargs = {
            'model_name': model_cls._meta.model_name
        }

        if method not in self.perms_map:
            raise exceptions.MethodNotAllowed(method)

        return [perm % kwargs for perm in self.perms_map[method]]
    
    def get_user_permissions(self, user):
        perms = []
        for group in user.groups.all():
            for permission in group.permissions.all():
                perms.append(permission.codename)
        
        return perms

    def has_perm(self, perm, obj):
        user_permissions = self.get_user_permissions(obj)
        return perm in user_permissions

    def has_perms(self, perm_list, obj=None):
        """
        Return True if the user has each of the specified permissions. If
        object is passed, check if the user has all required perms for it.
        """
        return any(self.has_perm(perm, obj) for perm in perm_list)

    def has_permission(self, request, view):
        perms = self.get_required_permissions(request.method, view.queryset.model)
        return self.has_perms(perms, request.user)


class PermissaoReceita(PermissaoCRUD):
    perms_map = {
        'GET': ['view_%(model_name)s'],
        'OPTIONS': ['view_%(model_name)s'],
        'HEAD': ['view_%(model_name)s'],
        'POST': ['add_%(model_name)s'],
        'PUT': ['change_%(model_name)s'],
        'PATCH': ['change_%(model_name)s'],
        'DELETE': ['delete_%(model_name)s'],
    }

    def has_permission(self, request, view):
        perms = self.get_required_permissions(request.method, Receita)
        return self.has_perms(perms, request.user)



class PermissaoDespesa(PermissaoCRUD):
    perms_map = {
        'GET': ['view_%(model_name)s'],
        'OPTIONS': ['view_%(model_name)s'],
        'HEAD': ['view_%(model_name)s'],
        'POST': ['add_%(model_name)s'],
        'PUT': ['change_%(model_name)s'],
        'PATCH': ['change_%(model_name)s'],
        'DELETE': ['delete_%(model_name)s'],
    }

    def has_permission(self, request, view):
        perms = self.get_required_permissions(request.method, Despesa)
        return self.has_perms(perms, request.user)


class PermissaoAssociacao(PermissaoCRUD):
    perms_map = {
        'GET': ['view_%(model_name)s'],
        'OPTIONS': ['view_%(model_name)s'],
        'HEAD': ['view_%(model_name)s'],
        'POST': ['add_%(model_name)s', 'change_%(model_name)s'],
        'PUT': ['change_%(model_name)s'],
        'PATCH': ['change_%(model_name)s'],
        'DELETE': ['delete_%(model_name)s', 'change_%(model_name)s'],
    }

    def has_permission(self, request, view):
        perms = self.get_required_permissions(request.method, Associacao)
        return self.has_perms(perms, request.user)


class PermissaoPrestacaoConta(PermissaoCRUD):
    perms_map = {
        'GET': ['view_%(model_name)s'],
        'OPTIONS': ['view_%(model_name)s'],
        'HEAD': ['view_%(model_name)s'],
        'POST': ['add_%(model_name)s'],
        'PUT': ['change_%(model_name)s'],
        'PATCH': ['change_%(model_name)s'],
        'DELETE': ['delete_%(model_name)s'],
    }

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            perms = self.get_required_permissions(request.method, PrestacaoConta)
            return self.has_perms(perms, request.user)
        return True


class PermissaoExportarDadosAssociacao(PermissaoCRUD):
    perms_map = {
        'GET': ['export_dados_associacao'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': [],
        'PUT': [],
        'PATCH': [],
        'DELETE': [],
    }

    def get_required_permissions(self, method):
        if method not in self.perms_map:
            raise exceptions.MethodNotAllowed(method)

        return [perm for perm in self.perms_map[method]]

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            perms = self.get_required_permissions(request.method)
            return self.has_perms(perms, request.user)
        return False


class PermissaoDashboardDre(PermissaoCRUD):
    perms_map = {
        'GET': ['view_dashboard_dre'],
        'OPTIONS': ['view_dashboard_dre'],
        'HEAD': ['view_dashboard_dre'],
        'POST': ['view_dashboard_dre'],
        'PUT': ['view_dashboard_dre'],
        'PATCH': ['view_dashboard_dre'],
        'DELETE': ['view_dashboard_dre'],
    }

    def get_required_permissions(self, method):
        if method not in self.perms_map:
            raise exceptions.MethodNotAllowed(method)

        return [perm for perm in self.perms_map[method]]

    def has_permission(self, request, view):
        perms = self.get_required_permissions(request.method)
        return self.has_perms(perms, request.user)


class PermissaoAssociacaoDre(PermissaoCRUD):
    perms_map = {
        'GET': ['view_associacao_dre'],
        'OPTIONS': ['view_associacao_dre'],
        'HEAD': ['view_associacao_dre'],
        'POST': ['view_associacao_dre'],
        'PUT': ['view_associacao_dre'],
        'PATCH': ['view_associacao_dre'],
        'DELETE': ['view_associacao_dre'],
    }

    def get_required_permissions(self, method):
        if method not in self.perms_map:
            raise exceptions.MethodNotAllowed(method)

        return [perm for perm in self.perms_map[method]]

    def has_permission(self, request, view):
        perms = self.get_required_permissions(request.method)
        return self.has_perms(perms, request.user)


class PermissaoDadosDiretoriaDre(PermissaoCRUD):
    perms_map = {
        'GET': ['view_dadosdiretoria_dre'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': [],
        'PUT': [],
        'PATCH': [],
        'DELETE': [],
    }

    def get_required_permissions(self, method):
        if method not in self.perms_map:
            raise exceptions.MethodNotAllowed(method)

        return [perm for perm in self.perms_map[method]]

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            perms = self.get_required_permissions(request.method)
            return self.has_perms(perms, request.user)
        return True