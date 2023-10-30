# Generated by Django 4.2.6 on 2023-10-27 20:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Admin_app', '0001_initial'),
        ('NativeApp', '0002_delete_availability'),
    ]

    operations = [
        migrations.AddField(
            model_name='worker',
            name='job_types',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Admin_app.typeofjobs'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='JobType',
        ),
    ]
