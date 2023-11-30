# Generated by Django 4.2.7 on 2023-11-29 19:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_rating_user_alter_rating_unique_together'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rating',
            old_name='product',
            new_name='post',
        ),
        migrations.RenameField(
            model_name='rating',
            old_name='stars',
            new_name='rating',
        ),
        migrations.AlterUniqueTogether(
            name='rating',
            unique_together=set(),
        ),
    ]