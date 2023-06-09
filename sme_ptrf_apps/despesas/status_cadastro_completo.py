# Status Choice
STATUS_COMPLETO = 'COMPLETO'
STATUS_INCOMPLETO = 'INCOMPLETO'
STATUS_INATIVO = 'INATIVO'

STATUS_NOMES = {
    STATUS_COMPLETO: 'Completo',
    STATUS_INCOMPLETO: 'Rascunho',
    STATUS_INATIVO: 'Inativo',
}

STATUS_CHOICES = (
    (STATUS_COMPLETO, STATUS_NOMES[STATUS_COMPLETO]),
    (STATUS_INCOMPLETO, STATUS_NOMES[STATUS_INCOMPLETO]),
    (STATUS_INATIVO, STATUS_NOMES[STATUS_INATIVO]),
)
