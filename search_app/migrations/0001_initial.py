# Generated by Django 5.1.1 on 2024-10-09 01:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(db_index=True, max_length=255)),
                ('description', models.TextField()),
                ('price', models.DecimalField(db_index=True, decimal_places=2, max_digits=10)),
                ('category', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='search_app.category')),
            ],
        ),
    ]
