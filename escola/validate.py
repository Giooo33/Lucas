import re
from validate_docbr import CPF
from django.core.exceptions import ValidationError

def validar_nota(valor):
    if float(valor) > 10:
        raise ValidationError('A nota não pode ser maior que 10.')
    

def telefone_validate(value):
    if not value.isdigit():
        raise ValidationError(
                ("%(value)s is not a valid phone number"),
                params={"value": value},
            )
    if len(value) != 11:

        raise ValidationError(
            ("%(value)s must be 11 digits"),
            params={"value": value},
        )
    return value


def cpf_validate(value):
    cpf = CPF()
    if not cpf.validate(value):
        raise ValidationError(
            ("%(value)s is not a valid CPF"),
            params={"value": value},
    )  


def cep_validate(value):
    if not re.match(r'^\d{5}-\d{3}$', value):
        raise ValidationError(
            ("%(value)s is not a valid CEP"),
            params={"value": value},
        )
    return value
