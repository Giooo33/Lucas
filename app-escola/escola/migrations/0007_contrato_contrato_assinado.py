# Generated by Django 5.1.8 on 2025-05-14 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('escola', '0006_contrato_contrato_pdf'),
    ]

    operations = [
        migrations.AddField(
            model_name='contrato',
            name='contrato_assinado',
            field=models.FileField(blank=True, null=True, upload_to='contratos_assinados/'),
        ),
    ]
