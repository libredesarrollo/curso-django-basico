# Generated by Django 3.0.4 on 2020-04-01 13:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('listelement', '0001_initial'),
        ('comment', '0009_comment_element'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='element',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='listelement.Element'),
        ),
    ]
