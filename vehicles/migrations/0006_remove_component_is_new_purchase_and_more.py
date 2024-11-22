# Generated by Django 5.1.3 on 2024-11-16 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0005_remove_component_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='component',
            name='is_new_purchase',
        ),
        migrations.RemoveField(
            model_name='component',
            name='price',
        ),
        migrations.RemoveField(
            model_name='vehicle',
            name='model',
        ),
        migrations.AddField(
            model_name='component',
            name='purchase_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='component',
            name='repair_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='issue',
            name='is_purchased',
            field=models.BooleanField(default=False),
        ),
        migrations.RemoveField(
            model_name='issue',
            name='component',
        ),
        migrations.AlterField(
            model_name='issue',
            name='description',
            field=models.TextField(default=2, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='issue',
            name='component',
            field=models.ManyToManyField(to='vehicles.component'),
        ),
    ]
