# Generated by Django 5.0 on 2024-01-06 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0004_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=255)),
                ('Description', models.CharField(max_length=255)),
                ('Price', models.CharField(max_length=255)),
                ('Stack', models.CharField(max_length=255)),
                ('Categogy_id', models.CharField(max_length=255)),
            ],
        ),
    ]
