# Generated by Django 5.1.4 on 2024-12-07 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0002_alter_attendee_options_remove_attendee_date_marked_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendee',
            name='is_adventist',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='No', max_length=3),
        ),
    ]
