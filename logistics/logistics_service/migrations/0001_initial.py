# Generated by Django 5.0.3 on 2024-03-20 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tracking',
            fields=[
                ('tracking_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('address', models.TextField()),
                ('status', models.TextField(choices=[('ordered', 'Ordered'), ('dispatched', 'Dispatched'), ('shiped', 'Shiped'), ('out_for_delivery', 'Out For Delivery'), ('delivered', 'Delivered'), ('picked_up', 'Picked Up'), ('return_to_seller', 'Return To Seller'), ('undelivered', 'Undelivered')], default='ordered')),
            ],
        ),
    ]
