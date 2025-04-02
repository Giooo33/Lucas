from django.contrib import admin
from escola.models import Responsavel, Aluno, Professor

class ResponsaveisAdmin(admin.ModelAdmin):
    list_display =('nome_responsavel', 'sobrenome_responsavel', 'numero_telefone_responsavel', 'email_responsavel', 'CPF_responsavel', 'data_nascimento_responsavel' )
    list_display_links = ('nome_responsavel', 'sobrenome_responsavel', 'numero_telefone_responsavel', 'email_responsavel')
    search_fields = ('nome_responsavel', 'sobrenome_responsavel')
    list_filter = ('nome_responsavel', 'sobrenome_responsavel')
    
    
class AlunoAdmin(admin.ModelAdmin):
    list_display =('nome_aluno', 'sobrenome_aluno', 'numero_telefone_aluno', 'email_aluno', 'numero_matricula_aluno', 'CPF_aluno', 'data_nascimento_aluno', 'class_choices' )
    list_display_links = ('nome_aluno', 'sobrenome_aluno', 'numero_telefone_aluno', 'email_aluno', 'numero_matricula_aluno')
    search_fields = ('nome_aluno', 'sobrenome_aluno')
    list_filter = ('nome_aluno', 'sobrenome_aluno')
    
    
    
    
class ProfessorAdmin(admin.ModelAdmin):
    list_display =('nome_professor', 'sobrenome_professor', 'numero_telefone_professor', 'email_professor', 'numero_matricula_professor', 'CPF_professor', 'data_nascimento_professor', 'class_choices' )
    list_display_links = ('nome_professor', 'sobrenome_professor', 'numero_telefone_professor', 'email_professor', 'numero_matricula_professor')
    search_fields = ('nome_professor', 'sobrenome_professor')
    list_filter = ('nome_professor', 'sobrenome_professor')
    
    
    
    
    
    #Registrar as classes no Django Admin
admin.site.register(Responsavel,  ResponsaveisAdmin)
admin.site.register(Aluno,  AlunoAdmin)
admin.site.register(Professor,  ProfessorAdmin)