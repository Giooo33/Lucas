# Este arquivo define os modelos (tabelas) do banco de dados da aplicação escolar.
# Cada classe representa uma entidade do sistema, com seus campos, validações e métodos auxiliares.
# Comentários detalhados explicam cada bloco, campo e método para facilitar a manutenção e o entendimento.

# Importações de módulos do Django e bibliotecas auxiliares para PDF, gráficos e validação
from django.db import models
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from django.core.files.base import ContentFile
from escola.validate import cpf_validate, telefone_validate, cep_validate, validar_nota, senha_validate
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt
import tempfile
from django.core.exceptions import ValidationError

# Modelo que representa uma turma escolar
class Turma(models.Model):
    # Opções de ano da turma
    TURMA_CHOICE = (
        ("1°", "1° Ano"),
        ("2°", "2° Ano"),
        ("3°", "3° Ano"),
    )  
    # Opções de itinerário formativo
    ITINERARIO_CHOICE = (
        ("DS", "Desenvolvimento de Sistemas"),
        ("CN", "Ciências da Natureza"),
        ("JG", "Jogos"),
    )
    # Nome da turma (ex: 1° Ano)
    turma_nome = models.CharField(max_length=50, choices=TURMA_CHOICE, verbose_name="Selecione a turma")
    # Nome do itinerário (ex: DS)
    itinerario_nome = models.CharField(max_length=50, choices=ITINERARIO_CHOICE, verbose_name="Selecione o itinerário")
    def __str__(self):
        return self.turma_nome + " " + self.itinerario_nome

# Modelo que representa uma matéria/disciplina
class Materia(models.Model):
    # Opções de matérias disponíveis
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
    # Nome da matéria
    materia_nome = models.CharField(max_length=50, choices=MATERIA_CHOICE, verbose_name="Selecione o itinerário")
    def __str__(self):
        return self.materia_nome


# Modelo que representa um aluno
class Aluno(models.Model):
    # Nome completo do aluno
    nome_aluno = models.CharField(max_length=200, verbose_name="Digite o nome do aluno completo.", null=True)
    # Telefone do aluno com validação customizada
    numero_telefone_aluno = models.CharField(max_length=15, validators=[telefone_validate], verbose_name="Digite o número do celular do aluno. (Formato: 629xxxxxxxx)")
    # E-mail do aluno
    email_aluno = models.EmailField(max_length=100, verbose_name="Digite o e-mail do aluno.")
    # CEP do aluno com validação customizada
    cep_aluno = models.CharField(max_length=100, validators=[cep_validate], verbose_name="Informe o Cep. (Formato xxxxx-xxx)", blank=False, null=True) 
    # CPF do aluno com validação customizada
    CPF_aluno = models.CharField(max_length=11, validators=[cpf_validate], verbose_name="Informe o CPF do aluno.", blank=False, null=True)
    # Data de nascimento do aluno
    data_nascimento_aluno = models.DateField(max_length=10, verbose_name="Digite a data de nascimento do aluno. (Formato xxxxx-xxx)")
    # Número de matrícula do aluno
    numero_matricula_aluno = models.CharField(max_length=6, verbose_name="Digite o número da matricula do aluno. (5 dígitos)")
    # Relação com a turma (chave estrangeira)
    class_choices = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name="turma_aluno", blank=False, null=True)    
    
    def __str__(self):
        return self.nome_aluno

# Modelo que representa um professor
class Professor(models.Model):
    # Nome completo do professor
    nome_professor = models.CharField(max_length=200, verbose_name="Digite o nome completo do professor.", null=True)
    # Número de telefone do professor, com validação de formato
    numero_telefone_professor = models.CharField(max_length=15, validators=[telefone_validate], verbose_name="Digite o número do celular do professor. (Formato: 629xxxxxxxx)")
    # E-mail do professor
    email_professor = models.EmailField(max_length=100, verbose_name="Digite o seu e-mail")
    # CEP do professor, com validação de formato
    cep_professor = models.CharField(max_length=100, validators=[cep_validate], verbose_name="Informe o Cep do professor. (Formato xxxxx-xxx)", blank=False, null=True) 
    # CPF do professor, com validação de formato
    CPF_professor = models.CharField(max_length=11, validators=[cpf_validate], verbose_name="Informe o CPF do professor.", blank=False, null=True)
    # Data de nascimento do professor
    data_nascimento_professor = models.DateField(max_length=10, verbose_name="Digite a data de nascimento do professor. (Formato aaaa-mm-dd)")
    # Número da matrícula do professor
    numero_matricula_professor = models.CharField(max_length=6, verbose_name="Digite o número da matricula do professor. (5 dígitos)")
    # Relação com a tabela Materia (chave estrangeira)
    subject_choices = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name="materia", blank=False, null=True) 
    # Relação com a tabela Turma (chave estrangeira)
    class_choices = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name="padrinho", blank=False, null=True)  
    # Senha de acesso do professor com validação customizada
    senha_de_acesso = models.CharField(max_length=5, validators=[senha_validate], verbose_name="Digite a senha de acesso do professor. (5 dígitos)", blank=False, null=True)
    # O ForeignKey é uma chave estrangeira que estabelece um relacionamento entre duas tabelas, permitindo que você vincule registros de uma tabela a registros de outra tabela. 
    # O parâmetro on_delete especifica o que acontece quando o registro relacionado é excluído. 
    # O related_name é o nome usado para referenciar o relacionamento reverso.
    def __str__(self):
        return self.nome_professor

# Modelo que representa as notas e desempenho de um aluno em uma matéria
class Nota_e_desempenho(models.Model):
    # Relação com a tabela Materia (chave estrangeira)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name="notas_materia", blank=False, null=True)
    # Relação com a tabela Professor (chave estrangeira)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name="notas_professor", blank=False, null=True)  # Corrigido related_name
    # Senha de acesso do professor, para validação
    senha_de_acesso_professor = models.CharField(max_length=5, validators=[senha_validate], verbose_name="Digite a senha de acesso do professor. (5 dígitos)", blank=False, null=True)
    # Notas dos bimestres, com validação de intervalo
    nota_1_bimestre = models.CharField(max_length=2, validators=[validar_nota], verbose_name="Nota do 1° Bimestre")
    nota_2_bimestre = models.CharField(max_length=2, validators=[validar_nota], verbose_name="Nota do 2° Bimestre")
    nota_3_bimestre = models.CharField(max_length=2, validators=[validar_nota], verbose_name="Nota do 3° Bimestre")
    nota_4_bimestre = models.CharField(max_length=2, validators=[validar_nota], verbose_name="Nota do 4° Bimestre")
    # Relação com a tabela Aluno (chave estrangeira)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="aluno_nota", blank=False, null=True)
    # Campo para armazenar o PDF do boletim
    boletim_pdf = models.FileField(upload_to='boletins/', blank=True, null=True)

    # Método para calcular a média das notas
    def calcular_media(self):
        """
        Calcula a média das quatro notas do aluno.
        """
        notas = [
            float(self.nota_1_bimestre),
            float(self.nota_2_bimestre),
            float(self.nota_3_bimestre),
            float(self.nota_4_bimestre),
        ]
        return round(sum(notas) / len(notas), 2)

    def __str__(self):
        return f"{self.aluno.nome_aluno} - {self.materia.materia_nome if self.materia else ''}"
    
    # Método para gerar gráfico de desempenho do aluno
    def gerar_grafico_desempenho(self):
        """
        Gera um gráfico de linha com o desempenho do aluno nos bimestres.
        """
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

    # Método para gerar o boletim em PDF
    def gerar_boletim_pdf(self):
        """
        Gera o boletim do aluno em PDF, salva no campo boletim_pdf e retorna o arquivo.
        """
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
        # Sempre sobrescreve o PDF, mesmo que já exista
        self.boletim_pdf.save(f"boletim_{self.aluno.nome_aluno}.pdf", ContentFile(buffer.read()), save=True)
        buffer.close()
        return self.boletim_pdf

    # Método alternativo para gerar o boletim em PDF, retornando o buffer
    def gerar_boletim_pdf_buffer(self):
        """
        Gera o boletim em PDF e retorna o buffer (BytesIO), sem salvar no banco.
        """
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
        return buffer

# Modelo que representa um responsável pelo aluno
class Responsavel(models.Model):
    # Nome completo do responsável
    nome_responsavel = models.CharField(max_length=200, verbose_name="Digite o nome do responsável completo.", null=True)
    # Telefone do responsável com validação customizada
    numero_telefone_responsavel = models.CharField(max_length=15, validators=[telefone_validate], verbose_name="Digite o número do celular do responsável. (Formato: 629xxxxxxxx)")
    # E-mail do responsável
    email_responsavel = models.EmailField(max_length=100, verbose_name="Digite o e-mail do responsável.")
    # CEP do responsável com validação customizada
    cep_responsavel = models.CharField(max_length=100, validators=[cep_validate], verbose_name="Informe o Cep. (Formato xxxxx-xxx)", blank=False, null=True) 
    # CPF do responsável com validação customizada
    CPF_responsavel = models.CharField(max_length=11, validators=[cpf_validate], verbose_name="Informe o CPF do responsável.", blank=False, null=True)
    # Data de nascimento do responsável
    data_nascimento_responsavel = models.DateField(max_length=10, verbose_name="Digite a data de nascimento do responsável. (Formato aaaa-mm-dd)")
    # Relação com o aluno (chave estrangeira)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="aluno_responsavel", blank=False, null=True)
    
    def __str__(self):
        return self.nome_responsavel
    

# Modelo que representa um contrato educacional
class Contrato(models.Model): 
    # Relação com a tabela Aluno (chave estrangeira)
    aluno = models.ForeignKey('Aluno', on_delete=models.CASCADE, related_name="contrato_aluno", blank=False, null=True)
    # Relação com a tabela Responsavel (chave estrangeira)
    responsavel = models.ForeignKey('Responsavel', on_delete=models.CASCADE, related_name="contrato_responsavel", blank=False, null=True)
    # Campo para armazenar o PDF do contrato
    contrato_pdf = models.FileField(upload_to='contratos/', blank=True, null=True)
    # Campo para armazenar o PDF do contrato assinado
    contrato_assinado = models.FileField(upload_to='contratos_assinados/', blank=True, null=True)  # Para o PDF assinado

    # Método para gerar o contrato em PDF
    def gerar_contrato_pdf(self):
        """
        Gera o contrato em PDF, salva no campo contrato_pdf e retorna o arquivo.
        """
        buffer = BytesIO()
        cnv = canvas.Canvas(buffer, pagesize=A4)
        cnv.setFont("Helvetica-Bold", 18)
        cnv.drawString(150, 800, "COLÉGIO EXEMPLO - CONTRATO EDUCACIONAL")
        cnv.setFont("Helvetica", 12)
        y = 770
        cnv.drawString(50, y, f"Aluno: {self.aluno.nome_aluno}")
        y -= 20
        cnv.drawString(50, y, f"Matrícula: {self.aluno.numero_matricula_aluno}")
        y -= 20
        cnv.drawString(50, y, f"Turma: {self.aluno.class_choices.turma_nome if self.aluno.class_choices else ''}")
        y -= 20
        cnv.drawString(50, y, f"Itinerário: {self.aluno.class_choices.itinerario_nome if self.aluno.class_choices else ''}")
        y -= 20
        cnv.drawString(50, y, f"Telefone: {self.aluno.numero_telefone_aluno}")
        y -= 20
        cnv.drawString(50, y, f"E-mail: {self.aluno.email_aluno}")
        y -= 20
        cnv.drawString(50, y, f"CEP: {self.aluno.cep_aluno}")
        y -= 20
        cnv.drawString(50, y, f"CPF: {self.aluno.CPF_aluno}")
        y -= 20
        cnv.drawString(50, y, f"Nascimento: {self.aluno.data_nascimento_aluno}")
        y -= 30
        cnv.setFont("Helvetica-Bold", 13)
        cnv.drawString(50, y, "Responsável Legal:")
        cnv.setFont("Helvetica", 12)
        y -= 20
        cnv.drawString(50, y, f"Nome: {self.responsavel.nome_responsavel}")
        y -= 20
        cnv.drawString(50, y, f"Telefone: {self.responsavel.numero_telefone_responsavel}")
        y -= 20
        cnv.drawString(50, y, f"E-mail: {self.responsavel.email_responsavel}")
        y -= 20
        cnv.drawString(50, y, f"CEP: {self.responsavel.cep_responsavel}")
        y -= 20
        cnv.drawString(50, y, f"CPF: {self.responsavel.CPF_responsavel}")
        y -= 20
        cnv.drawString(50, y, f"Nascimento: {self.responsavel.data_nascimento_responsavel}")
        y -= 40
        cnv.setFont("Helvetica-Bold", 13)
        cnv.drawString(50, y, "Cláusulas do Contrato:")
        cnv.setFont("Helvetica", 11)
        y -= 20
        # Lista de cláusulas do contrato
        clausulas = [
            "1. O presente contrato tem por objeto a prestação de serviços educacionais ao aluno acima qualificado, conforme calendário e regimento escolar.",
            "2. O responsável compromete-se a acompanhar a vida escolar do aluno, bem como a cumprir com as obrigações financeiras decorrentes da matrícula.",
            "3. O aluno e o responsável declaram estar cientes das normas disciplinares e pedagógicas da instituição.",
            "4. O não pagamento das mensalidades poderá acarretar sanções administrativas, conforme legislação vigente.",
            "5. O presente contrato tem validade para o ano letivo em curso, podendo ser renovado mediante novo acordo.",
            "6. As partes elegem o foro da comarca da instituição para dirimir eventuais dúvidas ou litígios." 
        ]
        for clausula in clausulas:
            cnv.drawString(50, y, clausula)
            y -= 15
        y -= 20
        cnv.setFont("Helvetica", 11)
        cnv.drawString(50, y, "Declaro, para os devidos fins, que li e estou de acordo com todas as cláusulas deste contrato.")
        y -= 40
        cnv.setFont("Helvetica", 12)
        cnv.drawString(50, y, "Assinatura do Responsável: ___________________________")
        y -= 30
        cnv.drawString(50, y, "Assinatura do Aluno: ________________________________")
        y -= 40
        from datetime import date
        cnv.setFont("Helvetica", 10)
        cnv.drawString(50, y, f"Local e data: ________________________, {date.today().strftime('%d/%m/%Y')}")
        cnv.showPage()
        cnv.save()
        buffer.seek(0)
        from django.core.files.base import ContentFile
        self.contrato_pdf.save(f"contrato_{self.id}.pdf", ContentFile(buffer.read()), save=True)
        buffer.close()
        return self.contrato_pdf

    # Método alternativo para gerar o contrato em PDF, retornando o buffer
    def gerar_contrato_pdf_buffer(self):
        """
        Gera o contrato em PDF e retorna o buffer (BytesIO), sem salvar no banco.
        """
        buffer = BytesIO()
        cnv = canvas.Canvas(buffer, pagesize=A4)
        cnv.setFont("Helvetica-Bold", 18)
        cnv.drawString(150, 800, "COLÉGIO EXEMPLO - CONTRATO EDUCACIONAL")
        cnv.setFont("Helvetica", 12)
        y = 770
        cnv.drawString(50, y, f"Aluno: {self.aluno.nome_aluno}")
        y -= 20
        cnv.drawString(50, y, f"Matrícula: {self.aluno.numero_matricula_aluno}")
        y -= 20
        cnv.drawString(50, y, f"Turma: {self.aluno.class_choices.turma_nome if self.aluno.class_choices else ''}")
        y -= 20
        cnv.drawString(50, y, f"Itinerário: {self.aluno.class_choices.itinerario_nome if self.aluno.class_choices else ''}")
        y -= 20
        cnv.drawString(50, y, f"Telefone: {self.aluno.numero_telefone_aluno}")
        y -= 20
        cnv.drawString(50, y, f"E-mail: {self.aluno.email_aluno}")
        y -= 20
        cnv.drawString(50, y, f"CEP: {self.aluno.cep_aluno}")
        y -= 20
        cnv.drawString(50, y, f"CPF: {self.aluno.CPF_aluno}")
        y -= 20
        cnv.drawString(50, y, f"Nascimento: {self.aluno.data_nascimento_aluno}")
        y -= 30
        cnv.setFont("Helvetica-Bold", 13)
        cnv.drawString(50, y, "Responsável Legal:")
        cnv.setFont("Helvetica", 12)
        y -= 20
        cnv.drawString(50, y, f"Nome: {self.responsavel.nome_responsavel}")
        y -= 20
        cnv.drawString(50, y, f"Telefone: {self.responsavel.numero_telefone_responsavel}")
        y -= 20
        cnv.drawString(50, y, f"E-mail: {self.responsavel.email_responsavel}")
        y -= 20
        cnv.drawString(50, y, f"CEP: {self.responsavel.cep_responsavel}")
        y -= 20
        cnv.drawString(50, y, f"CPF: {self.responsavel.CPF_responsavel}")
        y -= 20
        cnv.drawString(50, y, f"Nascimento: {self.responsavel.data_nascimento_responsavel}")
        y -= 40
        cnv.setFont("Helvetica-Bold", 13)
        cnv.drawString(50, y, "Cláusulas do Contrato:")
        cnv.setFont("Helvetica", 11)
        y -= 20
        clausulas = [
            "1. O presente contrato tem por objeto a prestação de serviços educacionais ao aluno acima qualificado, conforme calendário e regimento escolar.",
            "2. O responsável compromete-se a acompanhar a vida escolar do aluno, bem como a cumprir com as obrigações financeiras decorrentes da matrícula.",
            "3. O aluno e o responsável declaram estar cientes das normas disciplinares e pedagógicas da instituição.",
            "4. O não pagamento das mensalidades poderá acarretar sanções administrativas, conforme legislação vigente.",
            "5. O presente contrato tem validade para o ano letivo em curso, podendo ser renovado mediante novo acordo.",
            "6. As partes elegem o foro da comarca da instituição para dirimir eventuais dúvidas ou litígios." 
        ]
        for clausula in clausulas:
            cnv.drawString(50, y, clausula)
            y -= 15
        y -= 20
        cnv.setFont("Helvetica", 11)
        cnv.drawString(50, y, "Declaro, para os devidos fins, que li e estou de acordo com todas as cláusulas deste contrato.")
        y -= 40
        cnv.setFont("Helvetica", 12)
        cnv.drawString(50, y, "Assinatura do Responsável: ___________________________")
        y -= 30
        cnv.drawString(50, y, "Assinatura do Aluno: ________________________________")
        y -= 40
        from datetime import date
        cnv.setFont("Helvetica", 10)
        cnv.drawString(50, y, f"Local e data: ________________________, {date.today().strftime('%d/%m/%Y')}")
        cnv.showPage()
        cnv.save()
        buffer.seek(0)
        return buffer

    # Método para gerar gráfico de desempenho da turma
    def gerar_grafico_turma(self):
        """
        Gera um gráfico de barras com a média dos alunos da turma do contrato.
        """
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
        """
        Gera um gráfico de barras com a média dos alunos em uma disciplina específica.
        """
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
        """
        Retorna uma lista de alertas caso alguma nota ou a média final esteja abaixo de 6.
        """
        alertas = []
        notas = [float(self.nota_1_bimestre), float(self.nota_2_bimestre), float(self.nota_3_bimestre), float(self.nota_4_bimestre)]
        for i, nota in enumerate(notas, 1):
            if nota < 6:
                alertas.append(f'Atenção: Nota baixa no {i}º Bimestre!')
        if self.calcular_media() < 6:
            alertas.append('Atenção: Média final abaixo do esperado!')
        return alertas

    # Método para fazer upload do contrato assinado
    def upload_contrato_assinado(self, file):
        """
        Salva o arquivo PDF assinado no campo contrato_assinado.
        """
        self.contrato_assinado.save(f"contrato_assinado_{self.id}.pdf", file, save=True)
        return self.contrato_assinado

    # Método de validação personalizada
    def clean(self):
        """
        Validação customizada: garante que a senha informada corresponde ao professor selecionado.
        """
        super().clean()
        if self.professor and self.senha_de_acesso_professor:
            if self.professor.senha_de_acesso != self.senha_de_acesso_professor:
                raise ValidationError({'senha_de_acesso_professor': 'A senha não corresponde ao professor selecionado.'})