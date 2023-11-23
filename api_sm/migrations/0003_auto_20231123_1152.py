# Generated by Django 3.2.23 on 2023-11-23 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_sm', '0002_auto_20231123_1146'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dqe',
            name='deleted_at',
        ),
        migrations.RemoveField(
            model_name='historicaldqe',
            name='deleted_at',
        ),
        migrations.AddField(
            model_name='dqe',
            name='deleted',
            field=models.DateTimeField(db_index=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='dqe',
            name='deleted_by_cascade',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AddField(
            model_name='historicaldqe',
            name='deleted',
            field=models.DateTimeField(db_index=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='historicaldqe',
            name='deleted_by_cascade',
            field=models.BooleanField(default=False, editable=False),
        ),
    ]