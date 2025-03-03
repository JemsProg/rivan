# Generated by Django 5.1.5 on 2025-02-07 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TrainingQuotationRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.CharField(choices=[('CCNA', 'CCNA'), ('CCNP', 'CCNP'), ('CompTIA Security+', 'CompTIA Security+'), ('ITIL', 'ITIL')], max_length=50)),
                ('training_location', models.CharField(choices=[('Makati', 'Makati')], max_length=50)),
                ('delivery_mode', models.CharField(choices=[('F2F', 'Face-to-Face')], max_length=50)),
                ('number_of_attendees', models.PositiveIntegerField()),
                ('funding', models.CharField(choices=[('Personal/Individual', 'Personal/Individual'), ('Sponsor/Corporate', 'Sponsor/Corporate')], max_length=50)),
                ('voucher', models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], max_length=3)),
                ('full_name', models.CharField(max_length=100)),
                ('job_title', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('contact_number', models.CharField(max_length=15)),
                ('message', models.TextField(blank=True, null=True)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
