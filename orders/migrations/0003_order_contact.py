# Generated by Django 4.1.7 on 2023-04-11 13:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_user_email_is_verified_alter_user_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='contact',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.contact', verbose_name='Контакт'),
        ),
    ]
