from django.db import models
from validate_docbr import CPF
from django.core.exceptions import ValidationError

def cpf_validate(value):
    cpf = CPF()
    if not cpf.validate(value):
        raise ValidationError(
            ("%(value)s is not a valid CPF"),
            params={"value": value},
    )  

class Turma(models.Model):
    TURMA_CHOICE = (
        ("1", "1° Ano"),
        ("2", "2° Ano"),
        ("3", "3° Ano"),

    )  

    ITINERARIO_CHOICE = (
        ("DS", "Desenvolvimento de Sistemas"),
        ("CN", "Ciências da Natureza"),
        ("JG", "Jogos"),
    )

class Materia(models.Model):
    MATERIA_CHOICE = (
        ("Desenvolvimento de Sistemas"),
        ("Ciências da Natureza"),
        ("Jogos"),
        ("Matemática"),
        ("Português"),
        ("Educação Física"),
        ("História"),
        ("Geografia"),
        ("Artes"),
        ("Filosofia"),
        ("Sociologia"),
        ("Inglês"),
        ("Espanhol"),
    )

    turma_nome = models.CharField(max_length=50, choices=TURMA_CHOICE, verbose_name="Selecione a turma")
    itinerario_nome = models.CharField(max_length=50, choices=ITINERARIO_CHOICE, verbose_name="Selecione o itinerário")
    
        


class Responsavel(models.Model):
    nome_completo_responsavel = models.CharField(max_length=200, verbose_name="Digite o nome do responsável completo")
    numero_telefone_responsavel = models.CharField(max_length=15, verbose_name="Digite o número do celular (xx) xxxxx-xxxx")
    email_responsavel = models.EmailField(max_length=100, verbose_name="Digite o e-mail do responsável")
    adress = models.CharField(max_length=100) 
    CPF_responsavel = models.CharField(max_length=11, validators=[cpf_validate], verbose_name="Informe o CPF do responsável", blank=True, null=False)
    data_nascimento_responsavel = models.DateField(max_length=10, verbose_name="Digite a data de nascimento do responsável")
    
    def __str__(self):
        return self.nome_responsavel
    
class Aluno(models.Model):

    nome_completo_aluno = models.CharField(max_length=50, verbose_name="Digite o nome do aluno completo")
    numero_telefone_aluno = models.CharField(max_length=15, verbose_name="Digite o número do celular (xx) xxxxx-xxxx")
    email_aluno = models.EmailField(max_length=100, verbose_name="Digite o seu e-mail")
    adress = models.CharField(max_length=100) 
    CPF_aluno = models.CharField(max_length=11, validators=[cpf_validate], verbose_name="Informe o CPF do responsável", blank=True, null=False)
    data_nascimento_aluno = models.DateField(max_length=10, verbose_name="Digite a data de nascimento do aluno")
    numero_matricula_aluno = models.CharField(max_length=6, verbose_name="Digite o número da sua matricula")
    class_choices = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name="turma_aluno", blank=True, null=False) 
    
    def __str__(self):
        return self.nome_aluno
    

class Professor(models.Model):

    nome_completo_professor = models.CharField(max_length=50, verbose_name="Digite seu nome completo")
    numero_telefone_professor = models.CharField(max_length=15, verbose_name="Digite o número do celular (xx) xxxxx-xxxx")
    email_professor = models.EmailField(max_length=100, verbose_name="Digite o seu e-mail")
    adress = models.CharField(max_length=100) 
    CPF_professor = models.CharField(max_length=11, validators=[cpf_validate], verbose_name="Informe o CPF do responsável", blank=True, null=False)
    data_nascimento_professor = models.DateField(max_length=10, verbose_name="Digite a data de nascimento do professor")
    numero_matricula_professor = models.CharField(max_length=6, verbose_name="Digite o número da matricula")
    class_choices = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name="turma_professor", blank=True, null=False)    
    class_choices = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name="materia", blank=True, null=False) 


#O ForeignKey é uma chave estrangeira que estabelece um relacionamento entre duas tabelas, permitindo que você vincule registros de uma tabela a registros de outra tabela. 
# O parâmetro on_delete especifica o que acontece quando o registro relacionado é excluído. 
# O related_name é o nome usado para referenciar o relacionamento reverso.

    def __str__(self):
        return self.nome_professor
    
  
