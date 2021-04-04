# Generated by Django 3.1.7 on 2021-04-04 17:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AboutUser',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
                ('dob', models.DateField()),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('status', models.CharField(choices=[('S', 'Single'), ('IR', 'In a Relationship'), ('M', 'Married'), ('W', 'Widowed')], max_length=2)),
                ('occupation', models.CharField(choices=[('S', 'Student'), ('NAN', 'Invalid'), ('W', 'Worker'), ('E', 'Entrepreneur')], max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='UserGoals',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
                ('goal_1', models.CharField(max_length=200)),
                ('goal_2', models.CharField(max_length=200)),
                ('goal_3', models.CharField(max_length=200)),
                ('bio', models.CharField(max_length=600)),
            ],
        ),
        migrations.CreateModel(
            name='Events',
            fields=[
                ('event_id', models.AutoField(primary_key=True, serialize=False)),
                ('category', models.CharField(choices=[('S', 'SPORTS'), ('F', 'FUN'), ('E', 'Education'), ('O', 'Other')], default=('S', 'SPORTS'), max_length=3)),
                ('name', models.CharField(max_length=200)),
                ('image', models.FileField(upload_to='event_images')),
                ('location', models.CharField(choices=[('SCOT', 'Scotland'), ('ENGL', 'ENGLAND'), ('WALE', 'WALES'), ('IREL', 'IRELAND')], max_length=4)),
                ('event_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(unique=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EventParticipation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('participating', models.BooleanField()),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events_app.events')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
