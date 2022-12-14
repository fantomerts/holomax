# Generated by Django 3.2.7 on 2022-01-07 13:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0020_nuserprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nticket',
            name='qr_url',
        ),
        migrations.AddField(
            model_name='nticket',
            name='qr',
            field=models.ImageField(blank=True, help_text='Input a qr code of ticket', null=True, upload_to='ticket-qrs'),
        ),
        migrations.AlterField(
            model_name='nmovie',
            name='poster',
            field=models.ImageField(blank=True, help_text='Input a poster of movie', null=True, upload_to='movie-posters'),
        ),
        migrations.AlterField(
            model_name='nuserprofile',
            name='avatar',
            field=models.ImageField(upload_to='user-pics'),
        ),
        migrations.AlterField(
            model_name='nuserprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
