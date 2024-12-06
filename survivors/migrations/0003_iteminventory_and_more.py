# Generated by Django 5.1.2 on 2024-12-06 14:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survivors', '0002_remove_tradeitemrequested_trade_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemInventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(verbose_name='Quantidade')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
            ],
            options={
                'verbose_name': 'Item no Inventário',
                'verbose_name_plural': 'Itens no Inventário',
                'db_table': 'items_inventories',
            },
        ),
        migrations.RemoveIndex(
            model_name='inventory',
            name='inventories_survivo_1666a7_idx',
        ),
        migrations.RemoveIndex(
            model_name='inventory',
            name='inventories_quantit_e04d5a_idx',
        ),
        migrations.RemoveField(
            model_name='inventory',
            name='item',
        ),
        migrations.RemoveField(
            model_name='inventory',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='survivor',
            name='items',
        ),
        migrations.AlterField(
            model_name='inventory',
            name='survivor',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='survivors.survivor', verbose_name='Sobrevivente'),
        ),
        migrations.AddField(
            model_name='iteminventory',
            name='inventory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survivors.inventory', verbose_name='Inventário'),
        ),
        migrations.AddField(
            model_name='iteminventory',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survivors.item', verbose_name='Item'),
        ),
        migrations.AddField(
            model_name='inventory',
            name='items',
            field=models.ManyToManyField(through='survivors.ItemInventory', to='survivors.item'),
        ),
        migrations.AddIndex(
            model_name='inventory',
            index=models.Index(fields=['survivor'], name='inventories_survivo_d77233_idx'),
        ),
        migrations.AddIndex(
            model_name='iteminventory',
            index=models.Index(fields=['item'], name='items_inven_item_id_1e35ff_idx'),
        ),
        migrations.AddIndex(
            model_name='iteminventory',
            index=models.Index(fields=['inventory'], name='items_inven_invento_0cc93e_idx'),
        ),
        migrations.AddIndex(
            model_name='iteminventory',
            index=models.Index(fields=['quantity'], name='items_inven_quantit_ed9a28_idx'),
        ),
        migrations.AddIndex(
            model_name='iteminventory',
            index=models.Index(fields=['created_at', 'updated_at'], name='items_inven_created_19ddcd_idx'),
        ),
    ]
