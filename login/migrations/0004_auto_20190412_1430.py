# Generated by Django 2.2 on 2019-04-12 06:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_generateproblems_problems'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problems',
            name='op',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='operator', to='login.GenerateProblems'),
        ),
        migrations.AlterField(
            model_name='problems',
            name='scene',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='s', to='login.GenerateProblems'),
        ),
    ]
