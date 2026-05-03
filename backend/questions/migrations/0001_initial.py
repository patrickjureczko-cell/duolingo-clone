from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('MCQ', 'Multiple Choice'), ('FILL_BLANK', 'Fill in the Blank'), ('TRUE_FALSE', 'True or False'), ('FLASHCARD', 'Flashcard')], max_length=20)),
                ('text', models.TextField()),
                ('choices', models.JSONField(blank=True, null=True)),
                ('correct_answer', models.TextField()),
                ('explanation', models.TextField(blank=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='courses.unit')),
            ],
            options={'ordering': ['order']},
        ),
    ]
