from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('teachers', '0002_teacher_specialization'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='specialization',
            field=models.CharField(
                max_length=200,
                null=True,
                blank=True,
                verbose_name='Специализация (временно)',
            ),
        ),
    ]
