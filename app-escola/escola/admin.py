from django.contrib import admin
from escola.models import Responsavel, Aluno, Professor, Turma, Materia, Contrato

class TurmaAdmin(admin.ModelAdmin):
    list_display = ('id', 'turma_nome', 'itinerario_nome')
    search_fields = ('turma_nome', 'itinerario_nome',)
    list_filter = ('turma_nome', 'itinerario_nome',)
    
class MateriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'materia_nome')
    search_fields = ('materia_nome',)
    list_filter = ('materia_nome',)
   
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
    list_display =('aluno', 'responsavel', 'download_contrato')
    actions = ['download_contrato']
    list_display_links = ('aluno', 'responsavel', 'download_contrato')
    search_fields = ('aluno', 'responsavel',)
    list_filter = ('aluno', 'responsavel',)

#gerar um link para o downlaod do contrato   
    def download_contrato(self, request, queryset):
        for contrato in queryset:
            # Aqui você pode implementar a lógica para gerar o PDF do contrato
            # e retornar um link para download.
            pass
    download_contrato.short_description = "Download do Contrato"
    #Registrar as classes no Django Admin

admin.site.register(Contrato, ContratoAdmin)
admin.site.register(Turma, TurmaAdmin)
admin.site.register(Responsavel,  ResponsaveisAdmin)
admin.site.register(Aluno,  AlunoAdmin)
admin.site.register(Professor,  ProfessorAdmin)
admin.site.register(Materia, MateriaAdmin)