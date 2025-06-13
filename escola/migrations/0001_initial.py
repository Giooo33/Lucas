# Arquivo de migração inicial gerado automaticamente pelo Django.
# Define a estrutura inicial do banco de dados para o app 'escola'.
# Não é recomendado alterar manualmente este arquivo, pois ele é gerado pelo comando 'makemigrations'.
# As operações de criação de tabelas e campos iniciais são definidas aqui.
# Dependências: Nenhuma, pois é a primeira migração do app.

import django.db.models.deletion
import escola.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Responsavel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_responsavel', models.CharField(max_length=50, verbose_name='Digite o nome do responsável')),
                ('sobrenome_responsavel', models.CharField(max_length=50, verbose_name='Digite o sobrenome do responsável')),
                ('numero_telefone_responsavel', models.CharField(max_length=15, verbose_name='Digite o número do celular (xx) xxxxx-xxxx')),
                ('email_responsavel', models.EmailField(max_length=100, verbose_name='Digite o e-mail do responsável')),
                ('adress', models.CharField(max_length=100)),
                ('CPF_responsavel', models.CharField(blank=True, max_length=11, validators=[escola.models.cpf_validate], verbose_name='Informe o CPF do responsável')),
                ('data_nascimento_responsavel', models.DateField(max_length=10, verbose_name='Digite a data de nascimento do responsável')),
            ],
        ),
        migrations.CreateModel(
            name='Turma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('turma_nome', models.CharField(choices=[('1', '1° Ano'), ('2', '2° Ano'), ('3', '3° Ano')], max_length=50, verbose_name='Selecione a turma')),
                ('itinerario_nome', models.CharField(choices=[('DS', 'Desenvolvimento de Sistemas'), ('CN', 'Ciências da Natureza'), ('JG', 'Jogos')], max_length=50, verbose_name='Selecione o itinerário')),
            ],
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_professor', models.CharField(max_length=50, verbose_name='Digite seu nome')),
                ('sobrenome_professor', models.CharField(max_length=50, verbose_name='Digite o seu sobrenome')),
                ('numero_telefone_professor', models.CharField(max_length=15, verbose_name='Digite o número do celular (xx) xxxxx-xxxx')),
                ('email_professor', models.EmailField(max_length=100, verbose_name='Digite o seu e-mail')),
                ('adress', models.CharField(max_length=100)),
                ('CPF_professor', models.CharField(blank=True, max_length=11, validators=[escola.models.cpf_validate], verbose_name='Informe o CPF do responsável')),
                ('data_nascimento_professor', models.DateField(max_length=10, verbose_name='Digite a data de nascimento do professor')),
                ('numero_matricula_professor', models.CharField(max_length=6, verbose_name='Digite o número da matricula')),
                ('class_choices', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='turma_professor', to='escola.turma')),
            ],
        ),
        migrations.CreateModel(
            name='Aluno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_aluno', models.CharField(max_length=50, verbose_name='Digite o nome do aluno')),
                ('sobrenome_aluno', models.CharField(max_length=50, verbose_name='Digite o sobrenome do aluno')),
                ('numero_telefone_aluno', models.CharField(max_length=15, verbose_name='Digite o número do celular (xx) xxxxx-xxxx')),
                ('email_aluno', models.EmailField(max_length=100, verbose_name='Digite o seu e-mail')),
                ('adress', models.CharField(max_length=100)),
                ('CPF_aluno', models.CharField(blank=True, max_length=11, validators=[escola.models.cpf_validate], verbose_name='Informe o CPF do responsável')),
                ('data_nascimento_aluno', models.DateField(max_length=10, verbose_name='Digite a data de nascimento do aluno')),
                ('numero_matricula_aluno', models.CharField(max_length=6, verbose_name='Digite o número da sua matricula')),
                ('class_choices', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='turma_aluno', to='escola.turma')),
            ],
        ),
    ]
