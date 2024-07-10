# Generated by Django 5.0.6 on 2024-06-14 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_twitter_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='homepage_link',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='instagram_link',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='linkedin_link',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='profile_bio',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
