# Generated by Django 5.1.8 on 2025-05-14 14:36

import escola.validate
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('escola', '0009_alter_nota_e_desempenho_nota_1_bimestre_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nota_e_desempenho',
            name='nota_1_bimestre',
            field=models.CharField(max_length=2, validators=[escola.validate.validar_nota], verbose_name='Nota do 1° Bimestre'),
        ),
        migrations.AlterField(
            model_name='nota_e_desempenho',
            name='nota_2_bimestre',
            field=models.CharField(max_length=2, validators=[escola.validate.validar_nota], verbose_name='Nota do 2° Bimestre'),
        ),
        migrations.AlterField(
            model_name='nota_e_desempenho',
            name='nota_3_bimestre',
            field=models.CharField(max_length=2, validators=[escola.validate.validar_nota], verbose_name='Nota do 3° Bimestre'),
        ),
        migrations.AlterField(
            model_name='nota_e_desempenho',
            name='nota_4_bimestre',
            field=models.CharField(max_length=2, validators=[escola.validate.validar_nota], verbose_name='Nota do 4° Bimestre'),
        ),
    ]
