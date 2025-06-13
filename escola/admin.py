# Este arquivo customiza o painel administrativo do Django para os modelos da escola.
# Aqui são definidos quais campos aparecem, filtros, buscas, ações customizadas e botões para PDF.
# Cada classe abaixo representa a configuração de um modelo no admin.
# Recomenda-se manter comentários detalhados para facilitar manutenção e entendimento futuro.

# Importa o módulo de rotas do Django para adicionar URLs customizadas ao admin
from django.urls import path
# Importa o FileResponse para retornar arquivos (PDFs) como resposta HTTP
from django.http import FileResponse
# Importa constantes de tamanho de página do ReportLab para geração de PDFs
from reportlab.lib.pagesizes import A4
# Importa o canvas do ReportLab para desenhar no PDF
from reportlab.pdfgen import canvas
# Importa BytesIO para manipulação de arquivos em memória
from io import BytesIO
# Importa o módulo admin do Django para customizar o painel administrativo
from django.contrib import admin
# Importa HttpResponse para retornar respostas HTTP personalizadas
from django.http import HttpResponse
# Importa utilitário para renderizar HTML seguro no admin
from django.utils.html import format_html
# Importa o modelo Contrato do app atual
from .models import Contrato
# Importa todos os modelos necessários do app escola
from escola.models import Responsavel, Aluno, Professor, Turma, Materia, Contrato, Nota_e_desempenho
# Importa o módulo de formulários do Django (caso precise customizar formulários do admin)
from django import forms

# Classe de configuração do admin para o modelo Turma
class TurmaAdmin(admin.ModelAdmin):
    # Define os campos exibidos na listagem do admin
    list_display = ('id', 'turma_nome', 'itinerario_nome')
    # Permite busca pelos campos especificados
    search_fields = ('turma_nome', 'itinerario_nome',)
    # Permite filtrar pelos campos especificados
    list_filter = ('turma_nome', 'itinerario_nome',)
    
# Classe de configuração do admin para o modelo Materia
class MateriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'materia_nome')
    search_fields = ('materia_nome',)
    list_filter = ('materia_nome',)
   
# Classe de configuração do admin para o modelo Nota_e_desempenho
class Nota_e_desempenhoAdmin(admin.ModelAdmin):
    # Exibe os campos definidos na listagem do admin, incluindo métodos customizados
    list_display = ('id', 'aluno', 'professor', 'materia', 'nota_1_bimestre', 'nota_2_bimestre', 'nota_3_bimestre', 'nota_4_bimestre', 'media_aluno', 'botao_boletim')
    
    # Método para calcular e exibir a média do aluno na listagem
    def media_aluno(self, obj):
        return obj.calcular_media()
    # Define o nome da coluna no admin
    media_aluno.short_description = 'Média'

    # Cria um botão na listagem para gerar o boletim do aluno
    def botao_boletim(self, obj):
        return format_html('<a class="button" href="{}">Gerar Boletim</a>', f'gerar-boletim/{obj.id}/')
    botao_boletim.short_description = 'Boletim'

    # Adiciona URLs customizadas para ações específicas deste admin
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            # URL para gerar o boletim em PDF
            path('gerar-boletim/<int:nota_id>/', self.admin_site.admin_view(self.gerar_boletim), name='gerar_boletim'),
        ]
        return custom_urls + urls

    # Gera o boletim em PDF e retorna como resposta HTTP
    def gerar_boletim(self, request, nota_id):
        nota = Nota_e_desempenho.objects.get(pk=nota_id)
        nota.gerar_boletim_pdf()  # Gera e salva o PDF automaticamente
        return FileResponse(nota.boletim_pdf.open(), as_attachment=False, filename=f'boletim_{nota.aluno.nome_aluno}.pdf')

    # Ao salvar o modelo, gera automaticamente o boletim em PDF
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.gerar_boletim_pdf()  # Gera e salva o boletim automaticamente ao salvar a nota


# Classe de configuração do admin para o modelo Aluno
class AlunoAdmin(admin.ModelAdmin):
    # Define os campos exibidos na listagem do admin
    list_display =('nome_aluno', 'numero_telefone_aluno', 'email_aluno', 'numero_matricula_aluno', 'CPF_aluno', 'data_nascimento_aluno', 'class_choices', 'cep_aluno' )
    # Define quais campos são links para acessar o detalhe do registro
    list_display_links = ('nome_aluno', 'numero_telefone_aluno', 'email_aluno', 'numero_matricula_aluno')
    # Permite busca pelo nome do aluno
    search_fields = ('nome_aluno',)
    # Permite filtrar pelo nome do aluno
    list_filter = ('nome_aluno',)

# Classe de configuração do admin para o modelo Responsavel
class ResponsaveisAdmin(admin.ModelAdmin):
    list_display =('nome_responsavel', 'numero_telefone_responsavel', 'email_responsavel', 'CPF_responsavel', 'data_nascimento_responsavel', 'cep_responsavel' )
    list_display_links = ('nome_responsavel', 'numero_telefone_responsavel', 'email_responsavel')
    search_fields = ('nome_responsavel',)
    list_filter = ('nome_responsavel',)

# Classe de configuração do admin para o modelo Professor
class ProfessorAdmin(admin.ModelAdmin):
    list_display =('nome_professor', 'numero_telefone_professor', 'email_professor', 'numero_matricula_professor', 'CPF_professor', 'data_nascimento_professor', 'subject_choices', 'cep_professor' )
    list_display_links = ('nome_professor', 'numero_telefone_professor', 'email_professor', 'numero_matricula_professor')
    search_fields = ('nome_professor',)
    list_filter = ('nome_professor',)

# Classe de configuração do admin para o modelo Contrato
class ContratoAdmin(admin.ModelAdmin):
    # Exibe os campos definidos na listagem do admin
    list_display = ('aluno', 'responsavel', 'botao_abrir_contrato')
    # Permite busca por nome do aluno e do responsável
    search_fields = ('aluno__nome_aluno', 'responsavel__nome_responsavel')
    # Exclui o campo contrato_pdf do formulário do admin
    exclude = ('contrato_pdf',)

    # Cria um botão na listagem para abrir o contrato
    def botao_abrir_contrato(self, obj):
        return format_html('<a class="button" href="{}">Abrir Contrato</a>', f'visualizar-contrato/{obj.id}/')
    botao_abrir_contrato.short_description = 'Abrir Contrato'

    # Adiciona URLs customizadas para ações específicas deste admin
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            # URL para gerar o PDF do contrato
            path('gerar-pdf/<int:contrato_id>/', self.admin_site.admin_view(self.gerar_pdf), name='gerar_pdf'),
            # URL para visualizar o contrato (assinado ou não)
            path('visualizar-contrato/<int:contrato_id>/', self.admin_site.admin_view(self.visualizar_contrato_pdf), name='visualizar_contrato_pdf'),
            # URL para baixar o contrato
            path('baixar-contrato/<int:contrato_id>/', self.admin_site.admin_view(self.baixar_contrato_pdf), name='baixar_contrato_pdf'),
            # URL para upload do contrato assinado
            path('assinar-contrato/<int:contrato_id>/', self.admin_site.admin_view(self.assinar_contrato_view), name='assinar_contrato'),
        ]
        return custom_urls + urls

    # View para upload do contrato assinado pelo responsável
    def assinar_contrato_view(self, request, contrato_id):
        contrato = self.get_object(request, contrato_id)
        # Gera o PDF do contrato se ainda não existir
        if not contrato.contrato_pdf:
            contrato.gerar_contrato_pdf()
        # Se o método for POST e houver arquivo enviado, salva o contrato assinado
        if request.method == 'POST' and request.FILES.get('contrato_assinado'):
            contrato.contrato_assinado = request.FILES['contrato_assinado']
            contrato.save()
            return HttpResponse(f'<html><body>Contrato assinado enviado com sucesso!<br><a href="../visualizar-contrato/{contrato_id}/">Ver Contrato Assinado</a></body></html>')
        # Exibe o PDF do contrato e o formulário de upload juntos
        return HttpResponse(f"""
            <html><body>
            <h2>Assinar Contrato</h2>
            <object data='{contrato.contrato_pdf.url}' type='application/pdf' width='800' height='600'>
                <a href='{contrato.contrato_pdf.url}'>Baixar contrato</a>
            </object>
            <form method='post' enctype='multipart/form-data' style='margin-top:20px;'>
                <label>Envie o contrato assinado (PDF):</label><br>
                <input type='file' name='contrato_assinado' accept='application/pdf' required />
                <button type='submit'>Enviar Contrato Assinado</button>
            </form>
            </body></html>
        """)

    # Gera o PDF do contrato e retorna como resposta HTTP
    def gerar_pdf(self, request, contrato_id):
        contrato = self.get_object(request, contrato_id)
        contrato.gerar_contrato_pdf()
        return FileResponse(contrato.contrato_pdf.open(), as_attachment=False, filename=f'contrato_{contrato_id}.pdf')

    # Visualiza o PDF do contrato (assinado ou padrão)
    def visualizar_contrato_pdf(self, request, contrato_id):
        contrato = self.get_object(request, contrato_id)
        # Se houver contrato assinado, exibe ele; senão, exibe o contrato padrão
        if contrato.contrato_assinado and hasattr(contrato.contrato_assinado, 'open'):
            return FileResponse(contrato.contrato_assinado.open(), as_attachment=False, filename=f'contrato_assinado_{contrato_id}.pdf')
        if not contrato.contrato_pdf:
            contrato.gerar_contrato_pdf()
        return FileResponse(contrato.contrato_pdf.open(), as_attachment=False, filename=f'contrato_{contrato_id}.pdf')

    # Baixa o PDF do contrato
    def baixar_contrato_pdf(self, request, contrato_id):
        contrato = self.get_object(request, contrato_id)
        if not contrato.contrato_pdf:
            contrato.gerar_contrato_pdf()
        return FileResponse(contrato.contrato_pdf.open(), as_attachment=True, filename=f'contrato_{contrato_id}.pdf')

    # Abre o contrato em nova aba do navegador
    def baixar_abrir_contrato_view(self, request, contrato_id):
        contrato = self.get_object(request, contrato_id)
        if not contrato.contrato_pdf:
            contrato.gerar_contrato_pdf()
        pdf_url = contrato.contrato_pdf.url
        return HttpResponse(f'''<html><head><script>window.open('{pdf_url}', '_blank');</script></head><body>O contrato foi aberto em uma nova aba. Se não abrir, <a href="{pdf_url}" target="_blank">clique aqui</a>.</body></html>''')

    # Gera relatório gráfico de desempenho dos alunos selecionados
    def relatorio_desempenho(self, request, queryset):
        import tempfile
        import matplotlib.pyplot as plt
        from django.http import FileResponse
        from io import BytesIO
        buffer = BytesIO()
        plt.figure(figsize=(8,4))
        # Para cada objeto selecionado, plota as notas dos bimestres
        for obj in queryset:
            notas = [float(obj.nota_1_bimestre), float(obj.nota_2_bimestre), float(obj.nota_3_bimestre), float(obj.nota_4_bimestre)]
            plt.plot(['1º','2º','3º','4º'], notas, marker='o', label=obj.aluno.nome_aluno)
        plt.ylim(0, 10)
        plt.title('Desempenho dos Alunos Selecionados')
        plt.xlabel('Bimestre')
        plt.ylabel('Nota')
        plt.legend()
        temp = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        plt.savefig(temp.name, format='png')
        plt.close()
        temp.seek(0)
        buffer.write(temp.read())
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='relatorio_desempenho.png')

    # Descrição da ação customizada no admin
    relatorio_desempenho.short_description = 'Gerar gráfico de desempenho dos selecionados'

    # Lista de ações customizadas disponíveis no admin
    actions = ['relatorio_desempenho']

# Registra todos os modelos e suas configurações customizadas no admin do Django
admin.site.register(Nota_e_desempenho, Nota_e_desempenhoAdmin)
admin.site.register(Contrato, ContratoAdmin)
admin.site.register(Turma, TurmaAdmin)
admin.site.register(Responsavel,  ResponsaveisAdmin)
admin.site.register(Aluno,  AlunoAdmin)
admin.site.register(Professor,  ProfessorAdmin)
admin.site.register(Materia, MateriaAdmin)