# Generated by Django 2.0 on 2019-01-19 19:09

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('originalPrice', models.FloatField()),
                ('currentPrice', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('sku', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('brand', models.CharField(max_length=100)),
                ('image', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('category', models.CharField(choices=[('mb', 'Placas base'), ('cp', 'CPUs'), ('hd', 'Discos Duros'), ('gc', 'Tarjetas gráficas'), ('ra', 'RAM'), ('la', 'Portátiles'), ('gl', 'Portátiles Gaming'), ('sm', 'Smartphones'), ('tv', 'Televisores')], default='la', max_length=2)),
                ('averageRating', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='price',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product'),
        ),
    ]
