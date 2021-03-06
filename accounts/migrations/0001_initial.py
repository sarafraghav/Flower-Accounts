# Generated by Django 3.1.5 on 2021-06-24 07:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Cost_Center',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=100)),
                ('Description', models.CharField(max_length=50000)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Ledgers', to='accounts.company')),
            ],
        ),
        migrations.CreateModel(
            name='default_group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=2000)),
                ('type', models.BooleanField(verbose_name='Asset')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='financial_year',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(max_length=1000)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='financial_year', to='accounts.company')),
            ],
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Warehouse', to='accounts.company')),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Model', models.CharField(max_length=100)),
                ('Quantity', models.IntegerField()),
                ('Size', models.CharField(max_length=100)),
                ('Name', models.CharField(max_length=100)),
                ('Price', models.IntegerField()),
                ('Color', models.CharField(max_length=200)),
                ('Warehouse', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='accounts.warehouse')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Stock', to='accounts.company')),
            ],
        ),
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=1000)),
                ('Date', models.DateField()),
                ('Amount', models.IntegerField()),
                ('Cost_Center', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Receipt', to='accounts.cost_center')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Receipt', to='accounts.company')),
                ('fy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Receipt', to='accounts.financial_year')),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=1000)),
                ('Date', models.DateField()),
                ('Amount', models.IntegerField()),
                ('Cost_Center', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Purchase', to='accounts.cost_center')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Purchase', to='accounts.company')),
                ('fy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Purchase', to='accounts.financial_year')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Model', models.IntegerField()),
                ('Quantity', models.IntegerField()),
                ('Size', models.CharField(max_length=100)),
                ('Name', models.CharField(max_length=100)),
                ('Price', models.IntegerField()),
                ('Color', models.CharField(max_length=200)),
                ('Warehouse', models.CharField(max_length=200)),
                ('stock_id', models.IntegerField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Order', to='accounts.company')),
                ('fy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Order', to='accounts.financial_year')),
            ],
        ),
        migrations.CreateModel(
            name='Ledger',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Groups', to='accounts.company')),
                ('header', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Groups', to='accounts.default_group')),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numberoforders', models.IntegerField(default=0)),
                ('Itype', models.CharField(choices=[('cash', 'CASH'), ('creditbill', 'Credit Bill'), ('return', 'Goods Return')], default=('cash', 'CASH'), max_length=100)),
                ('Cost_Center', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Invoices', to='accounts.cost_center')),
                ('Orders', models.ManyToManyField(to='accounts.Order')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Invoice', to='accounts.company')),
                ('fy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Invoice', to='accounts.financial_year')),
            ],
        ),
        migrations.CreateModel(
            name='fyauth',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.financial_year')),
            ],
        ),
        migrations.AddField(
            model_name='cost_center',
            name='ltype',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Ledgers', to='accounts.ledger'),
        ),
        migrations.CreateModel(
            name='cauth',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.company')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
