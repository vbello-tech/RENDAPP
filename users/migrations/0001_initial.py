# Generated by Django 4.0.3 on 2022-07-05 10:46

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('services', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_pic', models.ImageField(blank=True, upload_to='Profile/')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('state', models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator('^\\d{4}-\\d{3}-\\d{4}$')])),
                ('city', models.CharField(blank=True, max_length=30, null=True)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
                ('is_a_provider', models.BooleanField(blank=True, default=False, null=True)),
                ('person', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceOwnerDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(blank=True, max_length=15, null=True)),
                ('city', models.CharField(blank=True, max_length=30, null=True)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
                ('proof_of_address', models.ImageField(upload_to='AddressProof/')),
                ('identity_proof', models.CharField(choices=[('NIN', 'NIN'), ('DRIVERS LICENSE', 'DRIVERS LICENSE')], max_length=100)),
                ('identity_proof_pic', models.ImageField(upload_to='IdentityProof/')),
                ('identity_proof_no', models.IntegerField()),
                ('bank_name', models.CharField(max_length=300)),
                ('bank_acc_number', models.IntegerField()),
                ('person', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RenderedServices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('negotiate', models.BooleanField(default=False, null=True)),
                ('service_ordered_date', models.DateTimeField(auto_now_add=True)),
                ('service_price', models.IntegerField()),
                ('completed_by_user', models.BooleanField(blank=True, default=False, null=True)),
                ('completed_by_provider', models.BooleanField(blank=True, default=False, null=True)),
                ('user_paid', models.BooleanField(blank=True, default=False, null=True)),
                ('provider_paid', models.BooleanField(blank=True, default=False, null=True)),
                ('ref_code', models.CharField(max_length=20)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('ordered_service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.service')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rendered_to', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderCompletedServices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('negotiate', models.BooleanField(default=False, null=True)),
                ('service_ordered_date', models.DateTimeField(auto_now_add=True)),
                ('service_price', models.IntegerField()),
                ('completed_by_user', models.BooleanField(blank=True, default=False, null=True)),
                ('completed_by_provider', models.BooleanField(blank=True, default=False, null=True)),
                ('user_paid', models.BooleanField(blank=True, default=False, null=True)),
                ('provider_paid', models.BooleanField(blank=True, default=False, null=True)),
                ('ref_code', models.CharField(max_length=20)),
                ('admin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rendered_by', to=settings.AUTH_USER_MODEL)),
                ('ordered_service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.service')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
