# Generated by Django 2.2.5 on 2019-11-10 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_auto_20191110_1741'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='attachment',
            field=models.FileField(null=True, upload_to='courses/%Y/%m/%d/'),
        ),
    ]