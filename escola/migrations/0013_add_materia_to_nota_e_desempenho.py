from django.db import migrations, models
import escola.validate

class Migration(migrations.Migration):
    dependencies = [
        ('escola', '0012_nota_e_desempenho_boletim_pdf'),
    ]

    operations = [
        migrations.AddField(
            model_name='nota_e_desempenho',
            name='materia',
            field=models.ForeignKey(null=True, on_delete=models.CASCADE, related_name='notas_materia', to='escola.materia'),
            preserve_default=False,
        ),
    ]
