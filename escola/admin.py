from django.urls import path
from django.http import FileResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from django.contrib import admin
from django.http import HttpResponse
from django.utils.html import format_html
from .models import Contrato
from escola.models import Responsavel, Aluno, Professor, Turma, Materia, Contrato, Nota_e_desempenho

class TurmaAdmin(admin.ModelAdmin):
    list_display = ('id', 'turma_nome', 'itinerario_nome')
    search_fields = ('turma_nome', 'itinerario_nome',)
    list_filter = ('turma_nome', 'itinerario_nome',)
    
class MateriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'materia_nome')
    search_fields = ('materia_nome',)
    list_filter = ('materia_nome',)
   
class Nota_e_desempenhoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nota_1_bimestre', 'nota_2_bimestre', 'nota_3_bimestre', 'nota_4_bimestre')

    def media(self, obj):
        return obj.calcular_media()

    media.short_description = 'Média'

    def botao_boletim(self, obj):
        return format_html('<a class="button" href="{}">Gerar Boletim</a>', f'gerar-boletim/{obj.id}/')

    botao_boletim.short_description = 'Boletim'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('gerar-boletim/<int:nota_id>/', self.admin_site.admin_view(self.gerar_boletim), name='gerar_boletim'),
        ]
        return custom_urls + urls

    def gerar_boletim(self, request, nota_id):
        nota = self.get_object(request, nota_id)
        boletim_pdf = nota.gerar_boletim_pdf()
        return FileResponse(boletim_pdf, as_attachment=True, filename=f'boletim_{nota.aluno.nome_aluno}.pdf')


class AlunoAdmin(admin.ModelAdmin):
    list_display =('nome_aluno', 'numero_telefone_aluno', 'email_aluno', 'numero_matricula_aluno', 'CPF_aluno', 'data_nascimento_aluno', 'class_choices', 'cep_aluno' )
    list_display_links = ('nome_aluno', 'numero_telefone_aluno', 'email_aluno', 'numero_matricula_aluno')
    search_fields = ('nome_aluno',)
    list_filter = ('nome_aluno',)

class ResponsaveisAdmin(admin.ModelAdmin):
    list_display =('nome_responsavel', 'numero_telefone_responsavel', 'email_responsavel', 'CPF_responsavel', 'data_nascimento_responsavel', 'cep_responsavel' )
    list_display_links = ('nome_responsavel', 'numero_telefone_responsavel', 'email_responsavel')
    search_fields = ('nome_responsavel',)
    list_filter = ('nome_responsavel',)

class ProfessorAdmin(admin.ModelAdmin):
    list_display =('nome_professor', 'numero_telefone_professor', 'email_professor', 'numero_matricula_professor', 'CPF_professor', 'data_nascimento_professor', 'subject_choices', 'cep_professor' )
    list_display_links = ('nome_professor', 'numero_telefone_professor', 'email_professor', 'numero_matricula_professor')
    search_fields = ('nome_professor',)
    list_filter = ('nome_professor',)

class ContratoAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'responsavel', 'download_contrato', 'upload_contrato_assinado', 'botao_gerar_pdf')
    search_fields = ('aluno__nome_aluno', 'responsavel__nome_responsavel')
    exclude = ('contrato_pdf', 'contrato_assinado') # Exclui os campos de upload do formulário

    def download_contrato(self, obj):
        if obj.contrato_pdf and hasattr(obj.contrato_pdf, 'url'):
            return format_html('<a href="{}" target="_blank">Download</a>', obj.contrato_pdf.url)
        return 'No contrato disponível'

    download_contrato.short_description = 'Download do Contrato'

    def upload_contrato_assinado(self, obj):
        if obj.contrato_assinado and hasattr(obj.contrato_assinado, 'url'):
            return format_html('<a href="{}" target="_blank">Ver Contrato Assinado</a>', obj.contrato_assinado.url)
        return 'Nenhum contrato assinado disponível'

    upload_contrato_assinado.short_description = 'Contrato Assinado'

    def botao_gerar_pdf(self, obj):
        return format_html('<a class="button" href="{}">Gerar PDF</a>', f'gerar-pdf/{obj.id}/')

    botao_gerar_pdf.short_description = 'Gerar PDF'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('gerar-pdf/<int:contrato_id>/', self.admin_site.admin_view(self.gerar_pdf), name='gerar_pdf'),
        ]
        return custom_urls + urls

    def gerar_pdf(self, request, contrato_id):
        contrato = self.get_object(request, contrato_id)
        contrato.gerar_contrato_pdf()  # Gera o PDF automaticamente
        return FileResponse(contrato.contrato_pdf.open(), as_attachment=True, filename=f'contrato_{contrato_id}.pdf')

admin.site.register(Nota_e_desempenho, Nota_e_desempenhoAdmin)
admin.site.register(Contrato, ContratoAdmin)
admin.site.register(Turma, TurmaAdmin)
admin.site.register(Responsavel,  ResponsaveisAdmin)
admin.site.register(Aluno,  AlunoAdmin)
admin.site.register(Professor,  ProfessorAdmin)
admin.site.register(Materia, MateriaAdmin)