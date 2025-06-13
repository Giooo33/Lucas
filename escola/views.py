# Importa funções utilitárias do Django para renderizar templates e redirecionar
from django.shortcuts import render, redirect
# Importa os modelos utilizados nas views
from .models import Professor, Turma, Materia, Aluno, Nota_e_desempenho, Contrato
# Importa utilitário para exibir mensagens ao usuário
from django.contrib import messages
# Importa classe para retornar respostas HTTP personalizadas
from django.http import HttpResponse

# View responsável pelo formulário de inserção de notas pelos professores
# Faz validação de senha, matéria e professor, e cadastra as notas se tudo estiver correto
# Exibe mensagens de erro ou sucesso conforme o caso
# Se for GET, exibe o formulário vazio
# Se for POST, processa o formulário e retorna o template com contexto atualizado

def acesso_inserir_notas(request):
    if request.method == 'POST' and 'aluno_id' in request.POST:
        professor_id = request.POST.get('professor_id')
        senha_professor = request.POST.get('senha_professor')
        materia_id = request.POST.get('materia_id')
        aluno_id = request.POST.get('aluno_id')
        nota1 = request.POST.get('nota_1_bimestre')
        nota2 = request.POST.get('nota_2_bimestre')
        nota3 = request.POST.get('nota_3_bimestre')
        nota4 = request.POST.get('nota_4_bimestre')
        # Validação: professor, matéria e senha
        try:
            professor = Professor.objects.get(id=professor_id)
            materia = Materia.objects.get(id=materia_id)
            # Verifica se a senha do professor está correta
            if professor.senha_de_acesso != senha_professor:
                messages.error(request, 'Senha do professor incorreta!')
            # Verifica se o professor leciona a matéria selecionada
            elif not hasattr(professor, 'materia') or str(professor.materia.id) != str(materia_id):
                messages.error(request, 'O professor selecionado não leciona esta matéria!')
            else:
                # Cria o registro de notas e desempenho
                Nota_e_desempenho.objects.create(
                    professor_id=professor_id,
                    materia_id=materia_id,
                    aluno_id=aluno_id,
                    nota_1_bimestre=nota1,
                    nota_2_bimestre=nota2,
                    nota_3_bimestre=nota3,
                    nota_4_bimestre=nota4
                )
                messages.success(request, 'Notas cadastradas com sucesso!')
                return redirect('acesso_inserir_notas')
        except Professor.DoesNotExist:
            messages.error(request, 'Professor não encontrado!')
        except Materia.DoesNotExist:
            messages.error(request, 'Matéria não encontrada!')
        # Recarrega o formulário com mensagens de erro e contexto atualizado
        professores = Professor.objects.all()
        materias = Materia.objects.all()
        alunos = Aluno.objects.all()
        return render(request, 'formulario_notas.html', {
            'professores': professores,
            'materias': materias,
            'alunos': alunos
        })
    # Se for GET, exibe o formulário de notas diretamente
    professores = Professor.objects.all()
    materias = Materia.objects.all()
    alunos = Aluno.objects.all()
    return render(request, 'formulario_notas.html', {
        'professores': professores,
        'materias': materias,
        'alunos': alunos
    })

# View para exibir o boletim em PDF diretamente no navegador
# Busca o registro de notas pelo id (pk), gera o PDF em memória e retorna como resposta HTTP inline
# O usuário visualiza o boletim sem baixar o arquivo

def visualizar_boletim(request, pk):
    """
    View para exibir o boletim em PDF no navegador.
    """
    nota = Nota_e_desempenho.objects.get(pk=pk)
    buffer = nota.gerar_boletim_pdf_buffer()
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="boletim.pdf"'
    return response

# View para exibir o contrato em PDF diretamente no navegador
# Busca o contrato pelo id (pk), gera o PDF em memória e retorna como resposta HTTP inline
# O usuário visualiza o contrato sem baixar o arquivo

def visualizar_contrato(request, pk):
    """
    View para exibir o contrato em PDF no navegador.
    """
    contrato = Contrato.objects.get(pk=pk)
    buffer = contrato.gerar_contrato_pdf_buffer()
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="contrato.pdf"'
    return response

# View para exibir a página de visualização do boletim, com links para visualizar e baixar o PDF
# Gera as URLs para visualização inline e download, e renderiza o template correspondente

def boletim_visualizacao(request, pk):
    """
    Página para exibir o boletim em PDF e oferecer download.
    """
    pdf_url = f"/boletim/{pk}/inline/"
    download_url = f"/boletim/{pk}/download/"
    return render(request, 'boletim_visualizacao.html', {'pdf_url': pdf_url, 'download_url': download_url})

# View para exibir o boletim em PDF inline (direto no navegador)
def boletim_inline(request, pk):
    nota = Nota_e_desempenho.objects.get(pk=pk)
    buffer = nota.gerar_boletim_pdf_buffer()
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="boletim.pdf"'
    return response

# View para download do boletim em PDF (força o download do arquivo)
def boletim_download(request, pk):
    nota = Nota_e_desempenho.objects.get(pk=pk)
    buffer = nota.gerar_boletim_pdf_buffer()
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="boletim.pdf"'
    return response
