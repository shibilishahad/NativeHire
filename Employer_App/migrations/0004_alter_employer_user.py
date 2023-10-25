# Generated by Django 4.2.6 on 2023-10-14 09:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('NativeApp', '0003_user_email_alter_user_phone_no'),
        ('Employer_App', '0003_alter_employer_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employer',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='NativeApp.user'),
        ),
    ]