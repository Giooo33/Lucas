from django.db import models
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from django.core.files.base import ContentFile
from escola.validate import cpf_validate, telefone_validate, cep_validate, validar_nota
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt
import tempfile

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
    boletim_pdf = models.FileField(upload_to='boletins/', blank=True, null=True)

    def calcular_media(self):
        notas = [
            float(self.nota_1_bimestre),
            float(self.nota_2_bimestre),
            float(self.nota_3_bimestre),
            float(self.nota_4_bimestre),
        ]
        return round(sum(notas) / len(notas), 2)

    def __str__(self):
        return f"Nota e Desempenho"
    
    def gerar_grafico_desempenho(self):
        notas = [float(self.nota_1_bimestre), float(self.nota_2_bimestre), float(self.nota_3_bimestre), float(self.nota_4_bimestre)]
        bimestres = ['1º', '2º', '3º', '4º']
        plt.figure(figsize=(5,3))
        plt.plot(bimestres, notas, marker='o', color='blue')
        plt.ylim(0, 10)
        plt.title(f'Desempenho de {self.aluno.nome_aluno}')
        plt.xlabel('Bimestre')
        plt.ylabel('Nota')
        plt.grid(True)
        temp = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        plt.savefig(temp.name, format='png')
        plt.close()
        return temp.name

    def gerar_boletim_pdf(self):
        buffer = BytesIO()
        cnv = canvas.Canvas(buffer, pagesize=A4)
        cnv.setFont("Helvetica-Bold", 18)
        cnv.drawString(180, 800, "BOLETIM ESCOLAR")
        cnv.setFont("Helvetica", 12)
        y = 760
        cnv.drawString(50, y, f"Nome do Aluno: {self.aluno.nome_aluno}")
        y -= 20
        cnv.drawString(50, y, f"Matrícula: {self.aluno.numero_matricula_aluno}")
        y -= 20
        cnv.drawString(50, y, f"Turma: {self.aluno.class_choices.turma_nome if self.aluno.class_choices else ''}")
        y -= 20
        cnv.drawString(50, y, f"Itinerário: {self.aluno.class_choices.itinerario_nome if self.aluno.class_choices else ''}")
        y -= 30
        cnv.setFont("Helvetica-Bold", 13)
        cnv.drawString(50, y, "Notas por Bimestre:")
        cnv.setFont("Helvetica", 12)
        y -= 20
        cnv.drawString(70, y, f"1º Bimestre: {self.nota_1_bimestre}")
        y -= 20
        cnv.drawString(70, y, f"2º Bimestre: {self.nota_2_bimestre}")
        y -= 20
        cnv.drawString(70, y, f"3º Bimestre: {self.nota_3_bimestre}")
        y -= 20
        cnv.drawString(70, y, f"4º Bimestre: {self.nota_4_bimestre}")
        y -= 30
        media = self.calcular_media()
        cnv.setFont("Helvetica-Bold", 12)
        cnv.drawString(50, y, f"Média Final: {media}")
        y -= 30
        # Alertas de notas baixas
        cnv.setFont("Helvetica", 11)
        for i, nota in enumerate([self.nota_1_bimestre, self.nota_2_bimestre, self.nota_3_bimestre, self.nota_4_bimestre], 1):
            if float(nota) < 6:
                cnv.setFillColorRGB(1,0,0)
                cnv.drawString(50, y, f"Atenção: Nota baixa no {i}º Bimestre!")
                cnv.setFillColorRGB(0,0,0)
                y -= 18
        if media < 6:
            cnv.setFillColorRGB(1,0,0)
            cnv.drawString(50, y, "Atenção: Média final abaixo do esperado!")
            cnv.setFillColorRGB(0,0,0)
            y -= 18
        # Gráfico de desempenho
        img_path = self.gerar_grafico_desempenho()
        cnv.drawImage(img_path, 320, 650, width=200, height=120)
        cnv.showPage()
        cnv.save()
        buffer.seek(0)
        from django.core.files.base import ContentFile
        if not self.boletim_pdf or not self.boletim_pdf.name:
            self.boletim_pdf.save(f"boletim_{self.aluno.nome_aluno}.pdf", ContentFile(buffer.read()), save=True)
        buffer.close()
        return self.boletim_pdf


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
        cnv.setFont("Helvetica-Bold", 18)
        cnv.drawString(180, 800, "CONTRATO EDUCACIONAL")
        cnv.setFont("Helvetica", 12)
        y = 760
        cnv.drawString(50, y, f"Nome do Aluno: {self.aluno.nome_aluno}")
        y -= 20
        cnv.drawString(50, y, f"Matrícula: {self.aluno.numero_matricula_aluno}")
        y -= 20
        cnv.drawString(50, y, f"Turma: {self.aluno.class_choices.turma_nome if self.aluno.class_choices else ''}")
        y -= 20
        cnv.drawString(50, y, f"Itinerário: {self.aluno.class_choices.itinerario_nome if self.aluno.class_choices else ''}")
        y -= 20
        cnv.drawString(50, y, f"Telefone do Aluno: {self.aluno.numero_telefone_aluno}")
        y -= 20
        cnv.drawString(50, y, f"E-mail do Aluno: {self.aluno.email_aluno}")
        y -= 20
        cnv.drawString(50, y, f"CEP do Aluno: {self.aluno.cep_aluno}")
        y -= 20
        cnv.drawString(50, y, f"CPF do Aluno: {self.aluno.CPF_aluno}")
        y -= 20
        cnv.drawString(50, y, f"Data de Nascimento do Aluno: {self.aluno.data_nascimento_aluno}")
        y -= 40
        cnv.setFont("Helvetica-Bold", 13)
        cnv.drawString(50, y, "Responsável:")
        cnv.setFont("Helvetica", 12)
        y -= 20
        cnv.drawString(50, y, f"Nome do Responsável: {self.responsavel.nome_responsavel}")
        y -= 20
        cnv.drawString(50, y, f"Telefone do Responsável: {self.responsavel.numero_telefone_responsavel}")
        y -= 20
        cnv.drawString(50, y, f"E-mail do Responsável: {self.responsavel.email_responsavel}")
        y -= 20
        cnv.drawString(50, y, f"CEP do Responsável: {self.responsavel.cep_responsavel}")
        y -= 20
        cnv.drawString(50, y, f"CPF do Responsável: {self.responsavel.CPF_responsavel}")
        y -= 20
        cnv.drawString(50, y, f"Data de Nascimento do Responsável: {self.responsavel.data_nascimento_responsavel}")
        y -= 40
        cnv.setFont("Helvetica-Bold", 13)
        cnv.drawString(50, y, "Termos do Contrato:")
        cnv.setFont("Helvetica", 11)
        y -= 20
        texto = (
            "O presente contrato estabelece as condições para a prestação de serviços educacionais, "
            "incluindo direitos e deveres das partes, formas de pagamento, frequência, avaliação e demais obrigações. "
            "O responsável declara estar ciente e de acordo com todas as cláusulas aqui descritas."
        )
        for linha in texto.split('. '):
            cnv.drawString(50, y, linha.strip())
            y -= 15
        y -= 30
        cnv.setFont("Helvetica", 12)
        cnv.drawString(50, y, "Assinatura do Responsável: ___________________________")
        y -= 30
        cnv.drawString(50, y, "Assinatura do Aluno: ________________________________")
        cnv.showPage()
        cnv.save()
        buffer.seek(0)
        from django.core.files.base import ContentFile
        # Sempre sobrescreve o arquivo
        self.contrato_pdf.save(f"contrato_{self.id}.pdf", ContentFile(buffer.read()), save=True)
        buffer.close()
        return self.contrato_pdf

    def gerar_grafico_turma(self):
        from .models import Nota_e_desempenho, Aluno
        turma = self.aluno.class_choices
        notas = Nota_e_desempenho.objects.filter(aluno__class_choices=turma)
        medias = [n.calcular_media() for n in notas]
        nomes = [n.aluno.nome_aluno for n in notas]
        plt.figure(figsize=(8,4))
        plt.bar(nomes, medias, color='orange')
        plt.ylim(0, 10)
        plt.title(f'Desempenho da Turma {turma.turma_nome}')
        plt.xlabel('Aluno')
        plt.ylabel('Média')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        temp = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        plt.savefig(temp.name, format='png')
        plt.close()
        return temp.name

    def gerar_grafico_disciplina(self, materia_nome):
        from .models import Nota_e_desempenho, Aluno
        notas = Nota_e_desempenho.objects.filter(aluno__class_choices__itinerario_nome=materia_nome)
        medias = [n.calcular_media() for n in notas]
        nomes = [n.aluno.nome_aluno for n in notas]
        plt.figure(figsize=(8,4))
        plt.bar(nomes, medias, color='green')
        plt.ylim(0, 10)
        plt.title(f'Desempenho na Disciplina {materia_nome}')
        plt.xlabel('Aluno')
        plt.ylabel('Média')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        temp = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        plt.savefig(temp.name, format='png')
        plt.close()
        return temp.name

    def relatorio_alertas(self):
        alertas = []
        notas = [float(self.nota_1_bimestre), float(self.nota_2_bimestre), float(self.nota_3_bimestre), float(self.nota_4_bimestre)]
        for i, nota in enumerate(notas, 1):
            if nota < 6:
                alertas.append(f'Atenção: Nota baixa no {i}º Bimestre!')
        if self.calcular_media() < 6:
            alertas.append('Atenção: Média final abaixo do esperado!')
        return alertas

    def upload_contrato_assinado(self, file):
        """
        Salva o arquivo PDF assinado no campo contrato_assinado.
        """
        self.contrato_assinado.save(f"contrato_assinado_{self.id}.pdf", file, save=True)
        return self.contrato_assinado