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
from django import forms

class TurmaAdmin(admin.ModelAdmin):
    list_display = ('id', 'turma_nome', 'itinerario_nome')
    search_fields = ('turma_nome', 'itinerario_nome',)
    list_filter = ('turma_nome', 'itinerario_nome',)
    
class MateriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'materia_nome')
    search_fields = ('materia_nome',)
    list_filter = ('materia_nome',)
   
class Nota_e_desempenhoAdmin(admin.ModelAdmin):
    list_display = ('id', 'aluno', 'nota_1_bimestre', 'nota_2_bimestre', 'nota_3_bimestre', 'nota_4_bimestre', 'media_aluno', 'botao_boletim')

    def media_aluno(self, obj):
        return obj.calcular_media()

    media_aluno.short_description = 'Média'

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
        nota = Nota_e_desempenho.objects.get(pk=nota_id)
        nota.gerar_boletim_pdf()  # Gera e salva o PDF automaticamente
        return FileResponse(nota.boletim_pdf.open(), as_attachment=True, filename=f'boletim_{nota.aluno.nome_aluno}.pdf')


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

class ContratoAssinadoForm(forms.ModelForm):
    class Meta:
        model = Contrato
        fields = ['contrato_assinado']

class ContratoAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'responsavel', 'visualizar_contrato', 'baixar_contrato', 'baixar_abrir_contrato', 'upload_contrato_assinado', 'botao_gerar_pdf')
    search_fields = ('aluno__nome_aluno', 'responsavel__nome_responsavel')
    exclude = ('contrato_pdf',)
    form = ContratoAssinadoForm

    def visualizar_contrato(self, obj):
        if obj.contrato_pdf and hasattr(obj.contrato_pdf, 'url'):
            return format_html('<a href="{}" target="_blank">Visualizar</a>', f"../visualizar-contrato/{obj.id}/")
        return 'Nenhum contrato disponível'
    visualizar_contrato.short_description = 'Visualizar Contrato'

    def baixar_contrato(self, obj):
        if obj.contrato_pdf and hasattr(obj.contrato_pdf, 'url'):
            return format_html('<a href="{}">Baixar</a>', f"../baixar-contrato/{obj.id}/")
        return 'Nenhum contrato disponível'
    baixar_contrato.short_description = 'Baixar Contrato'

    def upload_contrato_assinado(self, obj):
        if obj.contrato_assinado and hasattr(obj.contrato_assinado, 'url'):
            return format_html('<a href="{}" target="_blank">Ver Contrato Assinado</a>', obj.contrato_assinado.url)
        return 'Nenhum contrato assinado disponível'
    upload_contrato_assinado.short_description = 'Contrato Assinado'

    def botao_gerar_pdf(self, obj):
        return format_html('<a class="button" href="{}">Gerar PDF</a>', f'gerar-pdf/{obj.id}/')
    botao_gerar_pdf.short_description = 'Gerar PDF'

    def baixar_abrir_contrato(self, obj):
        if obj.contrato_pdf and hasattr(obj.contrato_pdf, 'url'):
            return format_html('<a href="{}">Baixar e Abrir</a>', f"../baixar-abrir-contrato/{obj.id}/")
        return 'Nenhum contrato disponível'
    baixar_abrir_contrato.short_description = 'Baixar e Abrir Contrato'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('gerar-pdf/<int:contrato_id>/', self.admin_site.admin_view(self.gerar_pdf), name='gerar_pdf'),
            path('visualizar-contrato/<int:contrato_id>/', self.admin_site.admin_view(self.visualizar_contrato_pdf), name='visualizar_contrato_pdf'),
            path('baixar-contrato/<int:contrato_id>/', self.admin_site.admin_view(self.baixar_contrato_pdf), name='baixar_contrato_pdf'),
            path('baixar-abrir-contrato/<int:contrato_id>/', self.admin_site.admin_view(self.baixar_abrir_contrato_view), name='baixar_abrir_contrato'),
        ]
        return custom_urls + urls

    def gerar_pdf(self, request, contrato_id):
        contrato = self.get_object(request, contrato_id)
        contrato.gerar_contrato_pdf()
        return FileResponse(contrato.contrato_pdf.open(), as_attachment=True, filename=f'contrato_{contrato_id}.pdf')

    def visualizar_contrato_pdf(self, request, contrato_id):
        contrato = self.get_object(request, contrato_id)
        if not contrato.contrato_pdf:
            contrato.gerar_contrato_pdf()
        return FileResponse(contrato.contrato_pdf.open(), as_attachment=False, filename=f'contrato_{contrato_id}.pdf')

    def baixar_contrato_pdf(self, request, contrato_id):
        contrato = self.get_object(request, contrato_id)
        if not contrato.contrato_pdf:
            contrato.gerar_contrato_pdf()
        return FileResponse(contrato.contrato_pdf.open(), as_attachment=True, filename=f'contrato_{contrato_id}.pdf')

    def baixar_abrir_contrato_view(self, request, contrato_id):
        contrato = self.get_object(request, contrato_id)
        if not contrato.contrato_pdf:
            contrato.gerar_contrato_pdf()
        pdf_url = contrato.contrato_pdf.url
        return HttpResponse(f'''<html><head><script>window.open('{pdf_url}', '_blank');</script></head><body>O contrato foi aberto em uma nova aba. Se não abrir, <a href="{pdf_url}" target="_blank">clique aqui</a>.</body></html>''')

    def relatorio_desempenho(self, request, queryset):
        import tempfile
        import matplotlib.pyplot as plt
        from django.http import FileResponse
        from io import BytesIO
        buffer = BytesIO()
        plt.figure(figsize=(8,4))
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

    relatorio_desempenho.short_description = 'Gerar gráfico de desempenho dos selecionados'

    actions = ['relatorio_desempenho']

admin.site.register(Nota_e_desempenho, Nota_e_desempenhoAdmin)
admin.site.register(Contrato, ContratoAdmin)
admin.site.register(Turma, TurmaAdmin)
admin.site.register(Responsavel,  ResponsaveisAdmin)
admin.site.register(Aluno,  AlunoAdmin)
admin.site.register(Professor,  ProfessorAdmin)
admin.site.register(Materia, MateriaAdmin)