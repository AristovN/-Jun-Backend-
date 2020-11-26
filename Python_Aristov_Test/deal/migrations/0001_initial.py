# Generated by Django 3.1.3 on 2020-11-23 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Deal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.CharField(max_length=128)),
                ('item', models.CharField(max_length=128)),
                ('total', models.PositiveIntegerField()),
                ('quantity', models.PositiveIntegerField()),
                ('date', models.DateTimeField()),
            ],
        ),
    ]