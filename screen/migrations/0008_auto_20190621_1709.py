# Generated by Django 2.2.2 on 2019-06-21 09:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('screen', '0007_auto_20190621_1356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='Interaction',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reply', to='screen.Comments', verbose_name='互动'),
        ),
    ]
