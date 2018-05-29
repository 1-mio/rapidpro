# Generated by Django 1.11.6 on 2017-11-16 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("msgs", "0110_remove_msg_has_template_error")]

    operations = [
        migrations.AddField(
            model_name="broadcast",
            name="metadata",
            field=models.TextField(help_text="The metadata for messages of this broadcast", null=True),
        ),
        migrations.AddField(
            model_name="msg", name="metadata", field=models.TextField(help_text="The metadata for this msg", null=True)
        ),
    ]
