# Generated by Django 4.1.2 on 2023-02-03 10:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'Category',
            },
        ),
        migrations.CreateModel(
            name='Consumer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=12, unique=True)),
                ('address', models.TextField()),
                ('email', models.EmailField(max_length=100)),
                ('gstin', models.CharField(max_length=15, unique=True)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'Consumer',
            },
        ),
        migrations.CreateModel(
            name='Description',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(max_length=255)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IMDAPP.category')),
            ],
            options={
                'db_table': 'Description',
            },
        ),
        migrations.CreateModel(
            name='NonCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'NonCategory',
            },
        ),
        migrations.CreateModel(
            name='NonDescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(max_length=255)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IMDAPP.noncategory')),
            ],
            options={
                'db_table': 'NonDescription',
            },
        ),
        migrations.CreateModel(
            name='NonPurchaseBill',
            fields=[
                ('billno', models.AutoField(primary_key=True, serialize=False)),
                ('time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'NonPurchaseBill',
            },
        ),
        migrations.CreateModel(
            name='NonSaleBill',
            fields=[
                ('billno', models.AutoField(primary_key=True, serialize=False)),
                ('time', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=150)),
                ('phone', models.CharField(max_length=12)),
                ('address', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=255)),
                ('Mode_of_delivery', models.CharField(max_length=50)),
                ('issued_to', models.CharField(max_length=50)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'NonSaleBill',
            },
        ),
        migrations.CreateModel(
            name='PurchaseBill',
            fields=[
                ('billno', models.AutoField(primary_key=True, serialize=False)),
                ('time', models.DateTimeField(auto_now=True)),
                ('consumer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchasesupplier', to='IMDAPP.consumer')),
            ],
            options={
                'db_table': 'PurchaseBill',
            },
        ),
        migrations.CreateModel(
            name='SaleBill',
            fields=[
                ('billno', models.AutoField(primary_key=True, serialize=False)),
                ('time', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=150)),
                ('phone', models.CharField(max_length=12)),
                ('address', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=255)),
                ('Mode_of_delivery', models.CharField(max_length=50)),
                ('issued_to', models.CharField(max_length=50)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'SaleBill',
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=12, unique=True)),
                ('address', models.TextField()),
                ('email', models.EmailField(max_length=100)),
                ('gstin', models.CharField(max_length=15, unique=True)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'Supplier',
            },
        ),
        migrations.CreateModel(
            name='trs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kdno', models.CharField(max_length=255)),
                ('sors_sink', models.CharField(max_length=255)),
                ('ref1', models.CharField(max_length=255)),
                ('ref2', models.CharField(max_length=255)),
                ('ref3', models.CharField(max_length=255)),
                ('unit_cost', models.CharField(max_length=255)),
                ('iss_srs', models.IntegerField()),
                ('trs_type', models.IntegerField()),
                ('qty_trs', models.DecimalField(blank=True, decimal_places=10, max_digits=20, null=True)),
                ('balance', models.DecimalField(blank=True, decimal_places=10, max_digits=20, null=True)),
            ],
            options={
                'db_table': 'trs',
            },
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'Unit',
            },
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subcategory', models.CharField(max_length=255)),
                ('is_consumable', models.BooleanField(default=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IMDAPP.category')),
            ],
            options={
                'db_table': 'Subcategory',
            },
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('billno', models.AutoField(primary_key=True, serialize=False)),
                ('time', models.DateTimeField(auto_now=True)),
                ('Mode_of_delivery', models.CharField(max_length=50)),
                ('label_code', models.CharField(default='', max_length=50)),
                ('condition', models.CharField(choices=[('GOOD', 'GOOD'), ('TORN', 'TORN'), ('DAMAGED', 'DAMAGED')], max_length=50)),
                ('quantity', models.IntegerField(default=1)),
                ('perprice', models.IntegerField(default=1)),
                ('totalprice', models.IntegerField(default=1)),
                ('is_deleted', models.BooleanField(default=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IMDAPP.category')),
                ('description', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IMDAPP.description')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IMDAPP.consumer')),
                ('subcategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IMDAPP.subcategory')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IMDAPP.unit')),
            ],
            options={
                'db_table': 'Stock',
            },
        ),
        migrations.CreateModel(
            name='SaleItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default='')),
                ('billno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='salebillno', to='IMDAPP.salebill')),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saleitem', to='IMDAPP.stock')),
            ],
            options={
                'db_table': 'SaleItem',
            },
        ),
        migrations.CreateModel(
            name='SaleBillDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('billno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saledetailsbillno', to='IMDAPP.salebill')),
            ],
            options={
                'db_table': 'SaleBillDetails',
            },
        ),
        migrations.CreateModel(
            name='PurchaseItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default='')),
                ('perprice', models.IntegerField(default='')),
                ('totalprice', models.IntegerField(default='')),
                ('is_deleted', models.BooleanField(default=False)),
                ('billno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchasebillno', to='IMDAPP.purchasebill')),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchaseitem', to='IMDAPP.stock')),
            ],
            options={
                'db_table': 'PurchaseItem',
            },
        ),
        migrations.CreateModel(
            name='PurchaseBillDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.CharField(blank=True, max_length=50, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('billno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchasedetailsbillno', to='IMDAPP.purchasebill')),
            ],
            options={
                'db_table': 'PurchaseBillDetails',
            },
        ),
        migrations.CreateModel(
            name='NonSubcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subcategory', models.CharField(max_length=255)),
                ('is_consumable', models.BooleanField(default=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IMDAPP.noncategory')),
            ],
            options={
                'db_table': 'NonSubcategory',
            },
        ),
        migrations.CreateModel(
            name='NonStock',
            fields=[
                ('billno', models.AutoField(primary_key=True, serialize=False)),
                ('time', models.DateTimeField(auto_now=True)),
                ('Mode_of_delivery', models.CharField(max_length=50)),
                ('label_code', models.CharField(default='', max_length=50)),
                ('condition', models.CharField(choices=[('GOOD', 'GOOD'), ('TORN', 'TORN'), ('DAMAGED', 'DAMAGED')], max_length=50)),
                ('quantity', models.IntegerField(default=1)),
                ('perprice', models.IntegerField(default=1)),
                ('totalprice', models.IntegerField(default=1)),
                ('is_deleted', models.BooleanField(default=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IMDAPP.noncategory')),
                ('description', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IMDAPP.nondescription')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IMDAPP.supplier')),
                ('subcategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IMDAPP.nonsubcategory')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IMDAPP.unit')),
            ],
            options={
                'db_table': 'NonStock',
            },
        ),
        migrations.CreateModel(
            name='NonSaleItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('billno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nonsalebillno', to='IMDAPP.nonsalebill')),
                ('nonstock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nonsaleitem', to='IMDAPP.nonstock')),
            ],
            options={
                'db_table': 'NonSaleItem',
            },
        ),
        migrations.CreateModel(
            name='NonSaleBillDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('billno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nonsaledetailsbillno', to='IMDAPP.nonsalebill')),
            ],
            options={
                'db_table': 'NonSaleBillDetails',
            },
        ),
        migrations.CreateModel(
            name='NonPurchaseItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default='')),
                ('perprice', models.IntegerField(default='')),
                ('totalprice', models.IntegerField(default='')),
                ('is_deleted', models.BooleanField(default=False)),
                ('billno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nonpurchasebillno', to='IMDAPP.nonpurchasebill')),
                ('nonstock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nonpurchaseitem', to='IMDAPP.nonstock')),
            ],
            options={
                'db_table': 'NonPurchaseItem',
            },
        ),
        migrations.CreateModel(
            name='NonPurchaseBillDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.CharField(blank=True, max_length=50, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('billno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nonpurchasedetailsbillno', to='IMDAPP.nonpurchasebill')),
            ],
            options={
                'db_table': 'NonPurchaseBillDetails',
            },
        ),
        migrations.AddField(
            model_name='nonpurchasebill',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nonpurchasesupplier', to='IMDAPP.supplier'),
        ),
        migrations.CreateModel(
            name='NonInwardBillDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.CharField(blank=True, max_length=50, null=True)),
                ('billno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='noninwarddetailsbillno', to='IMDAPP.nonstock')),
            ],
            options={
                'db_table': 'NonInwardBillDetails',
            },
        ),
        migrations.AddField(
            model_name='nondescription',
            name='subcategory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IMDAPP.nonsubcategory'),
        ),
        migrations.CreateModel(
            name='InwardBillDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.CharField(blank=True, max_length=50, null=True)),
                ('billno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inwarddetailsbillno', to='IMDAPP.stock')),
            ],
            options={
                'db_table': 'InwardBillDetails',
            },
        ),
        migrations.CreateModel(
            name='HNonStock',
            fields=[
                ('billno', models.AutoField(primary_key=True, serialize=False)),
                ('time', models.DateTimeField(auto_now=True)),
                ('Mode_of_delivery', models.CharField(max_length=50)),
                ('label_code', models.CharField(default='', max_length=50)),
                ('condition', models.CharField(choices=[('GOOD', 'GOOD'), ('TORN', 'TORN'), ('DAMAGED', 'DAMAGED')], max_length=50)),
                ('quantity', models.IntegerField(default=1)),
                ('perprice', models.IntegerField(default=1)),
                ('totalprice', models.IntegerField(default=1)),
                ('is_deleted', models.BooleanField(default=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IMDAPP.noncategory')),
                ('description', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IMDAPP.nondescription')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IMDAPP.supplier')),
                ('subcategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IMDAPP.nonsubcategory')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IMDAPP.unit')),
            ],
            options={
                'db_table': 'HNonStock',
            },
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('billno', models.AutoField(primary_key=True, serialize=False)),
                ('time', models.DateTimeField(auto_now=True)),
                ('Mode_of_delivery', models.CharField(max_length=50)),
                ('label_code', models.CharField(default='', max_length=50)),
                ('condition', models.CharField(choices=[('GOOD', 'GOOD'), ('TORN', 'TORN'), ('DAMAGED', 'DAMAGED')], max_length=50)),
                ('quantity', models.IntegerField(default=1)),
                ('perprice', models.IntegerField(default=1)),
                ('totalprice', models.IntegerField(default=1)),
                ('is_deleted', models.BooleanField(default=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IMDAPP.category')),
                ('description', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IMDAPP.description')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IMDAPP.consumer')),
                ('subcategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IMDAPP.subcategory')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IMDAPP.unit')),
            ],
            options={
                'db_table': 'History',
            },
        ),
        migrations.AddField(
            model_name='description',
            name='subcategory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IMDAPP.subcategory'),
        ),
    ]
