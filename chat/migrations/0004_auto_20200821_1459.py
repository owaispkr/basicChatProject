# Generated by Django 2.2 on 2020-08-21 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_message_room'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='room_description',
            field=models.TextField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='room',
            name='room',
            field=models.TextField(max_length=100),
        ),
    ]
