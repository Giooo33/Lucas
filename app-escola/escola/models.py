from django.db import models
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from django.core.files.base import ContentFile
from escola.validate import cpf_validate, telefone_validate, cep_validate, validar_nota
from reportlab.pdfgen import canvas

class Turma(models.Model):
    TURMA_CHOICE = (
        ("1°", "1° Ano"),
        ("2°", "2° Ano"),
        ("3°", "3° Ano"),

    )  

    ITINERARIO_CHOICE = (
        ("DS", "Desenvolvimento de Sistemas"),
        ("CN", "Ciências da Natureza"),
        ("JG", "Jogos"),
    )

    turma_nome = models.CharField(max_length=50, choices=TURMA_CHOICE, verbose_name="Selecione a turma")
    itinerario_nome = models.CharField(max_length=50, choices=ITINERARIO_CHOICE, verbose_name="Selecione o itinerário")

    def __str__(self):
        return self.turma_nome + " " + self.itinerario_nome

class Materia(models.Model):
    MATERIA_CHOICE = (
        ("DS", "Desenvolvimento de Sistemas"),
        ("CN", "Ciências da Natureza"),
        ("JG", "Jogos"),
        ("MAT", "Matemática"),
        ("PORT", "Português"),
        ("EF", "Educação Física"),
        ("HIST", "História"),
        ("GEO", "Geografia"),
        ("ART", "Artes"),
        ("FILO", "Filosofia"),
        ("SOCI", "Sociologia"),
        ("ING", "Inglês"),
        ("ESP", "Espanhol"),
    )

    materia_nome = models.CharField(max_length=50, choices=MATERIA_CHOICE, verbose_name="Selecione o itinerário")

    def __str__(self):
        return self.materia_nome


class Aluno(models.Model):

    nome_aluno = models.CharField(max_length=200, verbose_name="Digite o nome do aluno completo", null=True)
    numero_telefone_aluno = models.CharField(max_length=15, validators=[telefone_validate], verbose_name="Digite o número do celular (xx) xxxxx-xxxx")
    email_aluno = models.EmailField(max_length=100, verbose_name="Digite o seu e-mail")
    cep_aluno = models.CharField(max_length=100, validators=[cep_validate], verbose_name="Informe o Cep do responsavel", blank=False, null=True) 
    CPF_aluno = models.CharField(max_length=11, validators=[cpf_validate], verbose_name="Informe o CPF do responsável", blank=False, null=True)
    data_nascimento_aluno = models.DateField(max_length=10, verbose_name="Digite a data de nascimento do aluno")
    numero_matricula_aluno = models.CharField(max_length=6, verbose_name="Digite o número da sua matricula")
    class_choices = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name="turma_aluno", blank=False, null=True)    
    
    def __str__(self):
        return self.nome_aluno


class Nota_e_desempenho(models.Model):
    nota_1_bimestre = models.CharField(max_length=2, validators=[validar_nota], verbose_name="Nota do 1° Bimestre")
    nota_2_bimestre = models.CharField(max_length=2, validators=[validar_nota], verbose_name="Nota do 2° Bimestre")
    nota_3_bimestre = models.CharField(max_length=2, validators=[validar_nota], verbose_name="Nota do 3° Bimestre")
    nota_4_bimestre = models.CharField(max_length=2, validators=[validar_nota], verbose_name="Nota do 4° Bimestre")
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="aluno_nota", blank=False, null=True)

#calcular a média das notas
    def calcular_media(self):
        media_final = (self.nota_1_bimestre + self.nota_2_bimestre + self.nota_3_bimestre + self.nota_4_bimestre) / 4
        return media_final
    
    def __str__(self):
        return f"Nota e Desempenho"
    
    def calcular_media(self):
        # Calcula a média das notas
        notas = [
            float(self.nota_1_bimestre),
            float(self.nota_2_bimestre),
            float(self.nota_3_bimestre),
            float(self.nota_4_bimestre),
        ]
        return round(sum(notas) / len(notas), 2)

    def gerar_boletim_pdf(self):
        # Gera o boletim em PDF
        buffer = BytesIO()
        cnv = canvas.Canvas(buffer)

        # Título
        cnv.setFont("Helvetica-Bold", 16)
        cnv.drawString(200, 800, "Boletim Escolar")

        # Informações do aluno
        cnv.setFont("Helvetica", 12)
        cnv.drawString(50, 750, f"Nome do Aluno: {self.aluno.nome_aluno}")
        cnv.drawString(50, 730, f"Matrícula: {self.aluno.numero_matricula_aluno}")

        # Notas
        cnv.drawString(50, 700, "Notas:")
        cnv.drawString(70, 680, f"1° Bimestre: {self.nota_1_bimestre}")
        cnv.drawString(70, 660, f"2° Bimestre: {self.nota_2_bimestre}")
        cnv.drawString(70, 640, f"3° Bimestre: {self.nota_3_bimestre}")
        cnv.drawString(70, 620, f"4° Bimestre: {self.nota_4_bimestre}")

        # Média
        media = self.calcular_media()
        cnv.drawString(50, 590, f"Média Final: {media}")

        # Finaliza o PDF
        cnv.showPage()
        cnv.save()

        buffer.seek(0)
        return ContentFile(buffer.read(), f"boletim_{self.aluno.nome_aluno}.pdf")


class Responsavel(models.Model):

    nome_responsavel = models.CharField(max_length=200, verbose_name="Digite o nome do responsável completo", null=True)
    numero_telefone_responsavel = models.CharField(max_length=15, validators=[telefone_validate], verbose_name="Digite o número do celular (xx) xxxxx-xxxx")
    email_responsavel = models.EmailField(max_length=100, verbose_name="Digite o e-mail do responsável")
    cep_responsavel = models.CharField(max_length=100, validators=[cep_validate], verbose_name="Informe o Cep do responsavel", blank=False, null=True) 
    CPF_responsavel = models.CharField(max_length=11, validators=[cpf_validate], verbose_name="Informe o CPF do responsável", blank=False, null=True)
    data_nascimento_responsavel = models.DateField(max_length=10, verbose_name="Digite a data de nascimento do responsável")
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="aluno_responsavel", blank=False, null=True)
    
    def __str__(self):
        return self.nome_responsavel
    

class Professor(models.Model):

    nome_professor = models.CharField(max_length=200, verbose_name="Digite seu nome completo", null=True)
    numero_telefone_professor = models.CharField(max_length=15, validators=[telefone_validate], verbose_name="Digite o número do celular (xx) xxxxx-xxxx")
    email_professor = models.EmailField(max_length=100, verbose_name="Digite o seu e-mail")
    cep_professor = models.CharField(max_length=100, validators=[cep_validate], verbose_name="Informe o Cep do responsavel", blank=False, null=True) 
    CPF_professor = models.CharField(max_length=11, validators=[cpf_validate], verbose_name="Informe o CPF do responsável", blank=False, null=True)
    data_nascimento_professor = models.DateField(max_length=10, verbose_name="Digite a data de nascimento do professor")
    numero_matricula_professor = models.CharField(max_length=6, verbose_name="Digite o número da matricula")
    subject_choices = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name="materia", blank=False, null=True) 
    class_choices = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name="padrinho", blank=False, null=True)    


#O ForeignKey é uma chave estrangeira que estabelece um relacionamento entre duas tabelas, permitindo que você vincule registros de uma tabela a registros de outra tabela. 
# O parâmetro on_delete especifica o que acontece quando o registro relacionado é excluído. 
# O related_name é o nome usado para referenciar o relacionamento reverso.

    def __str__(self):
        return self.nome_professor

class Contrato(models.Model): 
    aluno = models.ForeignKey('Aluno', on_delete=models.CASCADE, related_name="contrato_aluno", blank=False, null=True)
    responsavel = models.ForeignKey('Responsavel', on_delete=models.CASCADE, related_name="contrato_responsavel", blank=False, null=True)
    contrato_pdf = models.FileField(upload_to='contratos/', blank=True, null=True)
    contrato_assinado = models.FileField(upload_to='contratos_assinados/', blank=True, null=True)  # Para o PDF assinado

    def gerar_contrato_pdf(self):
        buffer = BytesIO()
        cnv = canvas.Canvas(buffer, pagesize=A4)

        # Adiciona informações ao PDF
        eixo = 750
        cnv.drawString(100, eixo, f"Nome do Aluno: {self.aluno.nome_aluno}")
        eixo -= 20
        cnv.drawString(100, eixo, f"Telefone do Aluno: {self.aluno.numero_telefone_aluno}")
        eixo -= 20
        cnv.drawString(100, eixo, f"E-mail do Aluno: {self.aluno.email_aluno}")
        eixo -= 20
        cnv.drawString(100, eixo, f"CEP do Aluno: {self.aluno.cep_aluno}")
        eixo -= 20
        cnv.drawString(100, eixo, f"CPF do Aluno: {self.aluno.CPF_aluno}")
        eixo -= 20
        cnv.drawString(100, eixo, f"Data de Nascimento do Aluno: {self.aluno.data_nascimento_aluno}")
        eixo -= 40

        cnv.drawString(100, eixo, f"Nome do Responsável: {self.responsavel.nome_responsavel}")
        eixo -= 20
        cnv.drawString(100, eixo, f"Telefone do Responsável: {self.responsavel.numero_telefone_responsavel}")
        eixo -= 20
        cnv.drawString(100, eixo, f"E-mail do Responsável: {self.responsavel.email_responsavel}")
        eixo -= 20
        cnv.drawString(100, eixo, f"CEP do Responsável: {self.responsavel.cep_responsavel}")
        eixo -= 20
        cnv.drawString(100, eixo, f"CPF do Responsável: {self.responsavel.CPF_responsavel}")
        eixo -= 20
        cnv.drawString(100, eixo, f"Data de Nascimento do Responsável: {self.responsavel.data_nascimento_responsavel}")

        # Espaço para assinatura
        eixo -= 60
        cnv.drawString(100, eixo, "Assinatura do Responsável: ___________________________")
        eixo -= 40
        cnv.drawString(100, eixo, "Assinatura do Aluno: ________________________________")

        cnv.showPage()
        cnv.save()

        buffer.seek(0)
        self.contrato_pdf.save(f"contrato_{self.id}.pdf", ContentFile(buffer.read()))
        buffer.close()
        return self.contrato_pdf