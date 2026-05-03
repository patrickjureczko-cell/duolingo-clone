from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '0001_initial'),
        ('topics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.UUIDField()),
                ('xp', models.PositiveIntegerField(default=0)),
                ('streak_days', models.PositiveIntegerField(default=0)),
                ('last_active', models.DateField(blank=True, null=True)),
                ('hearts', models.PositiveIntegerField(default=5)),
                ('completed_units', models.ManyToManyField(blank=True, to='courses.unit')),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_progress', to='topics.topic')),
            ],
            options={'unique_together': {('session_id', 'topic')}},
        ),
    ]
