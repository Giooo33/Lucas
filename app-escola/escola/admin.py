from django.contrib import admin
from escola.models import Responsavel, Aluno, Professor, Turma, Materia

class ResponsaveisAdmin(admin.ModelAdmin):
    list_display =('nome_completo_responsavel', 'numero_telefone_responsavel', 'email_responsavel', 'CPF_responsavel', 'data_nascimento_responsavel' )
    list_display_links = ('nome_completo_responsavel', 'numero_telefone_responsavel', 'email_responsavel')
    search_fields = ('nome_completo_responsavel',)
    list_filter = ('nome_completo_responsavel',)

class TurmaAdmin(admin.ModelAdmin):
    list_display = ('id', 'turma_nome', 'itinerario_nome')
    search_fields = ('turma_nome', 'itinerario_nome',)
    list_filter = ('turma_nome', 'itinerario_nome',)
    
class MateriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'materia_nome')
    search_fields = ('materia_nome',)
    list_filter = ('materia_nome',)
   
class AlunoAdmin(admin.ModelAdmin):
    list_display =('nome_completo_aluno', 'numero_telefone_aluno', 'email_aluno', 'numero_matricula_aluno', 'CPF_aluno', 'data_nascimento_aluno', 'class_choices' )
    list_display_links = ('nome_completo_aluno', 'numero_telefone_aluno', 'email_aluno', 'numero_matricula_aluno')
    search_fields = ('nome_completo_aluno',)
    list_filter = ('nome_completo_aluno',)
    
class ProfessorAdmin(admin.ModelAdmin):
    list_display =('nome_completo_professor', 'numero_telefone_professor', 'email_professor', 'numero_matricula_professor', 'CPF_professor', 'data_nascimento_professor', 'subject_choices' )
    list_display_links = ('nome_completo_professor', 'numero_telefone_professor', 'email_professor', 'numero_matricula_professor')
    search_fields = ('nome_completo_professor',)
    list_filter = ('nome_completo_professor',)
    
    
    
    
    
    #Registrar as classes no Django Admin

admin.site.register(Turma, TurmaAdmin)
admin.site.register(Responsavel,  ResponsaveisAdmin)
admin.site.register(Aluno,  AlunoAdmin)
admin.site.register(Professor,  ProfessorAdmin)
admin.site.register(Materia, MateriaAdmin)