# Generated by Django 5.0 on 2024-01-02 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('profile_pic', models.FileField(default='sad.jpg', upload_to='customer_profile')),
                ('address', models.CharField(max_length=255)),
                ('mobile', models.CharField(max_length=255)),
            ],
        ),
    ]
