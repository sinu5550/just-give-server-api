# Generated by Django 5.0 on 2024-02-01 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_userprofile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(default='user/images/default.png', upload_to='user/images/'),
        ),
    ]