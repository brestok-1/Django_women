# Generated by Django 4.1.3 on 2022-12-07 20:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('women', '0004_category_women_cat'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['id'], 'verbose_name': 'Category', 'verbose_name_plural': "Categorie's"},
        ),
        migrations.AlterModelOptions(
            name='women',
            options={'ordering': ['-time_create', 'title'], 'verbose_name': 'Famous Women', 'verbose_name_plural': 'Famous Women'},
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(db_index=True, max_length=100, verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='women',
            name='cat',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='women.category', verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='women',
            name='content',
            field=models.TextField(blank=True, verbose_name="Article's content"),
        ),
        migrations.AlterField(
            model_name='women',
            name='title',
            field=models.CharField(max_length=250, verbose_name='Title'),
        ),
    ]