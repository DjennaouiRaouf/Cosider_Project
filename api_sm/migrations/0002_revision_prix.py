# Generated by Django 3.2.23 on 2023-11-22 09:15

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_currentuser.db.models.fields
import django_currentuser.middleware


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api_sm', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Revision_Prix',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designation', models.CharField(max_length=600)),
                ('unite', models.CharField(max_length=5)),
                ('prix_u', models.DecimalField(decimal_places=2, default=0, max_digits=38, validators=[django.core.validators.MinValueValidator(0)])),
                ('date_modification', models.DateTimeField(auto_now=True, db_column='Date_Modification')),
                ('dqe', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api_sm.dqe')),
                ('user_id', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Revision DQE',
                'verbose_name_plural': 'Revision DQE',
                'unique_together': {('dqe', 'designation', 'unite', 'prix_u')},
            },
        ),
    ]
