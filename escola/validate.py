# Este arquivo contém funções de validação customizadas para uso nos modelos Django.
# Cada função abaixo valida um tipo específico de dado (nota, telefone, CPF, CEP, senha).
# Caso o valor não seja válido, é lançada uma ValidationError, impedindo o salvamento do registro.

import re
from validate_docbr import CPF
from django.core.exceptions import ValidationError

# Valida se a nota está no intervalo permitido (0 a 10)
def validar_nota(valor):
    if float(valor) > 10:
        raise ValidationError('A nota não pode ser maior que 10.')
    # Não retorna erro se a nota for válida

# Valida se o telefone contém apenas dígitos e tem 11 caracteres (formato brasileiro)
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

# Valida se o CPF é válido usando a biblioteca validate_docbr
def cpf_validate(value):
    cpf = CPF()
    if not cpf.validate(value):
        raise ValidationError(
            ("%(value)s is not a valid CPF"),
            params={"value": value},
    )  

# Valida se o CEP está no formato 00000-000
def cep_validate(value):
    if not re.match(r'^\d{5}-\d{3}$', value):
        raise ValidationError(
            ("%(value)s is not a valid CEP"),
            params={"value": value},
        )
    return value

# Valida se a senha contém apenas dígitos e tem exatamente 5 caracteres
def senha_validate(value):
    if not value.isdigit():
        raise ValidationError(
            ("A senha deve conter apenas dígitos"),
            params={"value": value},
        )
    if len(value) != 5:
        raise ValidationError(
            ("A senha deve conter exatamente 5 números"),
            params={"value": value},
        )
    return value
