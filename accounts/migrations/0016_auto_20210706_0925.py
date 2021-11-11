# Generated by Django 3.1.5 on 2021-07-06 03:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_auto_20210630_2046'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='money_account',
            field=models.ForeignKey(default=8, on_delete=django.db.models.deletion.CASCADE, related_name='Purchase_money_account', to='accounts.cost_center'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='receipt',
            name='money_account',
            field=models.ForeignKey(default=8, on_delete=django.db.models.deletion.CASCADE, related_name='Receipt_money_account', to='accounts.cost_center'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='Orders',
            field=models.ManyToManyField(related_name='Invoice', to='accounts.Order'),
        ),
    ]
