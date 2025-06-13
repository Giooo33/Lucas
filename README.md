# Sistema Escolar Django

Este projeto foi desenvolvido por uma aluna como parte de um estudo/prática de programação com Django. O objetivo é simular um sistema escolar completo, com cadastro de alunos, professores, turmas, matérias, contratos e boletins.

## Funcionalidades principais
- Cadastro e gerenciamento de alunos, professores, responsáveis, turmas e matérias.
- Lançamento de notas por professores, com validação de senha e vínculo com a matéria.
- Geração automática de boletins em PDF para cada aluno, incluindo gráficos de desempenho.
- Geração de contratos educacionais em PDF, com possibilidade de upload do contrato assinado.
- Visualização e download de boletins e contratos diretamente pelo sistema.
- Validações customizadas para CPF, telefone, CEP, notas e senha de acesso.
- **Segurança no lançamento de notas:** Para cadastrar as notas, o professor precisa informar sua senha. O sistema verifica se a senha corresponde ao professor cadastrado e se o nome e a disciplina também estão corretos. Só assim o professor tem acesso ao cadastro das notas, garantindo mais segurança e autenticidade no processo.

## Estrutura do código
- **models.py**: Define as tabelas do banco de dados (aluno, professor, turma, matéria, nota, contrato, responsável) e métodos auxiliares para geração de PDFs e gráficos.
- **admin.py**: Customiza o painel administrativo do Django, adicionando botões, filtros, buscas e ações customizadas para facilitar a gestão escolar.
- **views.py**: Implementa as páginas e rotas do sistema, como formulários de notas, visualização de boletins e contratos.
- **validate.py**: Funções de validação para garantir que os dados inseridos estejam corretos.
- **templates/**: Contém os arquivos HTML usados nas páginas do sistema.
- **migrations/**: Arquivos de migração do banco de dados.

## Como rodar o projeto
1. Instale as dependências do Python listadas em `requirements.txt`.
2. Execute as migrações do Django para criar o banco de dados:
   ```bash
   python manage.py migrate
   ```
3. Crie um superusuário para acessar o admin:
   ```bash
   python manage.py createsuperuser
   ```
4. Rode o servidor de desenvolvimento:
   ```bash
   python manage.py runserver
   ```

## Observações
- O sistema foi feito para fins didáticos e pode ser expandido com novas funcionalidades.
- O código está comentado para facilitar o entendimento de outros alunos e professores.
- **Observação importante:** A ideia de segurança para o lançamento de notas (verificação de senha, nome e disciplina do professor) foi implementada, mas não funcionou corretamente em todos os casos. Recomenda-se revisar e aprimorar essa parte para garantir total segurança.


