# Generated by Django 5.1.2 on 2024-12-12 14:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(verbose_name='Descrição')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
            ],
            options={
                'verbose_name': 'Denúncia',
                'verbose_name_plural': 'Denúncias',
                'db_table': 'reports',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Água', 'Água'), ('Comida', 'Comida'), ('Medicação', 'Medicação'), ('Munição', 'Munição')], max_length=100, verbose_name='Nome')),
                ('points', models.PositiveIntegerField(verbose_name='Pontos')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
            ],
            options={
                'verbose_name': 'Item',
                'verbose_name_plural': 'Itens',
                'db_table': 'items',
                'indexes': [models.Index(fields=['name'], name='items_name_dd4454_idx')],
            },
        ),
        migrations.CreateModel(
            name='ItemInventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(verbose_name='Quantidade')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survivors.item', verbose_name='Item')),
            ],
            options={
                'verbose_name': 'Item no Inventário',
                'verbose_name_plural': 'Itens no Inventário',
                'db_table': 'items_inventories',
            },
        ),
        migrations.CreateModel(
            name='Survivor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nome')),
                ('date_of_birth', models.DateField(verbose_name='Data de Nascimento')),
                ('sex', models.CharField(choices=[('M', 'Masculino'), ('F', 'Feminino'), ('O', 'Outro')], max_length=1, verbose_name='Sexo')),
                ('latitude', models.FloatField(verbose_name='Latitude')),
                ('longitude', models.FloatField(verbose_name='Longitude')),
                ('infected', models.BooleanField(default=False, verbose_name='Infectado')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('reports', models.ManyToManyField(through='survivors.Report', to='survivors.survivor', verbose_name='Denúncias')),
            ],
            options={
                'verbose_name': 'Sobrevivente',
                'verbose_name_plural': 'Sobreviventes',
                'db_table': 'survivors',
            },
        ),
        migrations.AddField(
            model_name='report',
            name='reported',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reported', to='survivors.survivor', verbose_name='Denunciado'),
        ),
        migrations.AddField(
            model_name='report',
            name='reporter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reporter', to='survivors.survivor', verbose_name='Denunciante'),
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('items', models.ManyToManyField(related_name='items', to='survivors.iteminventory', verbose_name='Items')),
                ('survivor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='survivors.survivor', verbose_name='Sobrevivente')),
            ],
            options={
                'verbose_name': 'Inventário',
                'verbose_name_plural': 'Inventários',
                'db_table': 'inventories',
            },
        ),
        migrations.AddIndex(
            model_name='iteminventory',
            index=models.Index(fields=['item'], name='items_inven_item_id_1e35ff_idx'),
        ),
        migrations.AddIndex(
            model_name='iteminventory',
            index=models.Index(fields=['quantity'], name='items_inven_quantit_ed9a28_idx'),
        ),
        migrations.AddIndex(
            model_name='iteminventory',
            index=models.Index(fields=['created_at', 'updated_at'], name='items_inven_created_19ddcd_idx'),
        ),
        migrations.AddIndex(
            model_name='survivor',
            index=models.Index(fields=['name', 'date_of_birth'], name='survivors_name_6bad2d_idx'),
        ),
        migrations.AddIndex(
            model_name='survivor',
            index=models.Index(fields=['latitude', 'longitude'], name='survivors_latitud_e6b27a_idx'),
        ),
        migrations.AddIndex(
            model_name='survivor',
            index=models.Index(fields=['infected'], name='survivors_infecte_0ba5fe_idx'),
        ),
        migrations.AddIndex(
            model_name='survivor',
            index=models.Index(fields=['created_at', 'updated_at'], name='survivors_created_0ff70a_idx'),
        ),
        migrations.AddIndex(
            model_name='report',
            index=models.Index(fields=['reporter', 'reported'], name='reports_reporte_a8e1b6_idx'),
        ),
        migrations.AddIndex(
            model_name='inventory',
            index=models.Index(fields=['survivor'], name='inventories_survivo_d77233_idx'),
        ),
        migrations.AddIndex(
            model_name='inventory',
            index=models.Index(fields=['created_at', 'updated_at'], name='inventories_created_35d6b6_idx'),
        ),
    ]
