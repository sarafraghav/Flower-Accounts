# Generated by Django 3.1.5 on 2021-06-29 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_df'),
    ]

    operations = [
        migrations.AlterField(
            model_name='default_group',
            name='type',
            field=models.CharField(choices=[('Capital Account', 'Capital Account'), ('Loans(Liability)', 'Loans(Liability)'), ('Current Liabilities', 'Current Liabilities'), ('Fixed Assets', 'Fixed Assets'), ('Investments', 'Investments'), ('Current Assets', 'Current Assets'), ('Branch Divisions', 'Branch Divisions'), ('Suspense AC', 'Suspense AC'), ('Sales Account', 'Sales Account'), ('Purchase Accounts', 'Purchase Accounts'), ('Direct Incomes', 'Direct Incomes'), ('Direct Expenses', 'Direct Expenses'), ('Indirect Incomes', 'Indirect Incomes'), ('Indirect Expenses', 'Indirect Expenses')], default=('Capital Account', 'Capital Account'), max_length=100),
        ),
        migrations.DeleteModel(
            name='df',
        ),
        migrations.DeleteModel(
            name='dg',
        ),
    ]
