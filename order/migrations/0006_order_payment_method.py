# Generated by Django 3.2.6 on 2021-10-08 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_auto_20211008_1335'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('Cash on Delivery', 'Cash on Delivery'), ('Paypal', 'Paypal')], default='Cash on Delivery', max_length=30),
        ),
    ]