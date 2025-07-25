# Generated by Django 5.2.3 on 2025-07-01 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InformacaoEmpresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('razao_social', models.CharField(help_text='Razão social da empresa', max_length=255, verbose_name='Razão Social')),
                ('nome_fantasia', models.CharField(help_text='Nome fantasia da empresa', max_length=255, verbose_name='Nome Fantasia')),
                ('cnpj', models.CharField(help_text='CNPJ da empresa (formato: XX.XXX.XXX/XXXX-XX)', max_length=18, verbose_name='CNPJ')),
                ('logradouro', models.CharField(help_text='Endereço da empresa', max_length=255, verbose_name='Logradouro')),
                ('numero', models.CharField(help_text='Número do endereço', max_length=20, verbose_name='Número')),
                ('complemento', models.CharField(blank=True, help_text='Complemento do endereço', max_length=100, null=True, verbose_name='Complemento')),
                ('cep', models.CharField(help_text='CEP (formato: XXXXX-XXX)', max_length=9, verbose_name='CEP')),
                ('bairro', models.CharField(help_text='Bairro da empresa', max_length=100, verbose_name='Bairro')),
                ('municipio', models.CharField(help_text='Município da empresa', max_length=100, verbose_name='Município')),
                ('uf', models.CharField(help_text='Estado (UF) da empresa', max_length=2, verbose_name='UF')),
                ('email', models.EmailField(help_text='E-mail de contato da empresa', max_length=254, verbose_name='E-mail')),
                ('telefone', models.CharField(help_text='Telefone de contato da empresa', max_length=20, verbose_name='Telefone')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('atualizado_em', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
            ],
            options={
                'verbose_name': 'Informação da Empresa',
                'verbose_name_plural': 'Informações da Empresa',
            },
        ),
    ]
