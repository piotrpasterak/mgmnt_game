
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='games', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(auto_now=True)),
                ('total_time', models.FloatField(blank=True, null=True)),
                ('seed', models.IntegerField(blank=True, null=True)),
                ('possibilities', models.TextField(blank=True, null=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rounds', to='process.Game')),
            ],
        ),
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(auto_now=True)),
                ('total_time', models.FloatField(blank=True, null=True)),
                ('seed', models.IntegerField(blank=True, null=True)),
                ('player_choice', models.TextField(blank=True, null=True)),
                ('real_values', models.TextField(blank=True, null=True)),
                ('cost', models.FloatField(blank=True, null=True)),
                ('risk', models.FloatField(blank=True, null=True)),
                ('expected_profit', models.FloatField(blank=True, null=True)),
                ('expected_return', models.FloatField(blank=True, null=True)),
                ('real_profit', models.FloatField(blank=True, null=True)),
                ('real_return', models.FloatField(blank=True, null=True)),
                ('parent_round', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='steps', to='process.Round')),
            ],
        ),
    ]
