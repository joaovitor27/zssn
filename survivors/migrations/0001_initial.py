# Generated by Django 5.1.2 on 2024-10-13 13:45

import django.db.models.deletion
from django.db import migrations, models


def create_items(apps, schema_editor):
    item = apps.get_model('survivors', 'Item')
    item.objects.bulk_create([
        item(name='Água', points=4),
        item(name='Comida', points=3),
        item(name='Medicação', points=2),
        item(name='Munição', points=1),
    ])


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
                ('name', models.CharField(choices=[('Água', 'Água'), ('Comida', 'Comida'), ('Medicação', 'Medicação'),
                                                   ('Munição', 'Munição')], max_length=100, verbose_name='Nome')),
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
        migrations.RunPython(create_items),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(verbose_name='Quantidade')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survivors.item',
                                           verbose_name='Item')),
            ],
            options={
                'verbose_name': 'Inventário',
                'verbose_name_plural': 'Inventários',
                'db_table': 'inventories',
            },
        ),
        migrations.CreateModel(
            name='Survivor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nome')),
                ('date_of_birth', models.DateField(verbose_name='Data de Nascimento')),
                ('sex', models.CharField(choices=[('M', 'Masculino'), ('F', 'Feminino'), ('O', 'Outro')], max_length=1,
                                         verbose_name='Sexo')),
                ('latitude', models.FloatField(verbose_name='Latitude')),
                ('longitude', models.FloatField(verbose_name='Longitude')),
                ('infected', models.BooleanField(default=False, verbose_name='Infectado')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('items',
                 models.ManyToManyField(through='survivors.Inventory', to='survivors.item', verbose_name='Itens')),
                ('reports',
                 models.ManyToManyField(through='survivors.Report', to='survivors.survivor', verbose_name='Denúncias')),
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
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reported',
                                    to='survivors.survivor', verbose_name='Denunciado'),
        ),
        migrations.AddField(
            model_name='report',
            name='reporter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reporter',
                                    to='survivors.survivor', verbose_name='Denunciante'),
        ),
        migrations.AddField(
            model_name='inventory',
            name='survivor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survivors.survivor',
                                    verbose_name='Sobrevivente'),
        ),
        migrations.CreateModel(
            name='Trade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False, verbose_name='Status')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('requested', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requested',
                                                to='survivors.survivor', verbose_name='Solicitado')),
                ('requester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requester',
                                                to='survivors.survivor', verbose_name='Solicitante')),
            ],
            options={
                'verbose_name': 'Troca',
                'verbose_name_plural': 'Trocas',
                'db_table': 'trades',
            },
        ),
        migrations.CreateModel(
            name='TradeItemRequested',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(verbose_name='Quantidade')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survivors.item',
                                           verbose_name='Item')),
                ('trade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survivors.trade',
                                            verbose_name='Troca')),
            ],
            options={
                'verbose_name': 'Item do Solicitado',
                'verbose_name_plural': 'Itens do Solicitado',
                'db_table': 'trade_items_requested',
            },
        ),
        migrations.AddField(
            model_name='trade',
            name='items_requested',
            field=models.ManyToManyField(related_name='items_requested', through='survivors.TradeItemRequested',
                                         to='survivors.item', verbose_name='Itens Solicitado'),
        ),
        migrations.CreateModel(
            name='TradeItemRequester',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(verbose_name='Quantidade')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survivors.item',
                                           verbose_name='Item')),
                ('trade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survivors.trade',
                                            verbose_name='Troca')),
            ],
            options={
                'verbose_name': 'Item do Solicitante',
                'verbose_name_plural': 'Itens do Solicitante',
                'db_table': 'trade_items_requester',
            },
        ),
        migrations.AddField(
            model_name='trade',
            name='items_requester',
            field=models.ManyToManyField(related_name='items_requester', through='survivors.TradeItemRequester',
                                         to='survivors.item', verbose_name='Itens Solicitante'),
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
            index=models.Index(fields=['survivor', 'item'], name='inventories_survivo_1666a7_idx'),
        ),
        migrations.AddIndex(
            model_name='inventory',
            index=models.Index(fields=['quantity'], name='inventories_quantit_e04d5a_idx'),
        ),
        migrations.AddIndex(
            model_name='inventory',
            index=models.Index(fields=['created_at', 'updated_at'], name='inventories_created_35d6b6_idx'),
        ),
        migrations.AddIndex(
            model_name='trade',
            index=models.Index(fields=['requester', 'requested'], name='trades_request_a68bec_idx'),
        ),
        migrations.AddIndex(
            model_name='trade',
            index=models.Index(fields=['status'], name='trades_status_425b31_idx'),
        ),
        migrations.AddIndex(
            model_name='trade',
            index=models.Index(fields=['created_at', 'updated_at'], name='trades_created_01a4e7_idx'),
        ),
    ]