# Generated by Django 2.1.2 on 2019-10-09 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidates', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='candidates',
            options={'verbose_name': 'Candidate', 'verbose_name_plural': 'Candidates'},
        ),
        migrations.AlterModelOptions(
            name='terms',
            options={'ordering': ['county', 'type', 'id'], 'verbose_name': 'Term', 'verbose_name_plural': 'Terms'},
        ),
        migrations.AddField(
            model_name='terms',
            name='status',
            field=models.CharField(db_index=True, default='', max_length=100),
        ),
    ]
