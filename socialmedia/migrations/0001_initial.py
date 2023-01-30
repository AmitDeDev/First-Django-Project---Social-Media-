# Generated by Django 4.0.2 on 2022-05-09 18:36

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
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=200)),
                ('dob', models.DateField()),
                ('imageUrl', models.CharField(blank=True, default='https://www.adobe.com/express/create/media_127540366421d3d5bfcaf8202527ca7d37741fd5d.jpeg?width=400&format=jpeg&optimize=medium', max_length=3000, null=True)),
                ('coverUrl', models.CharField(blank=True, default='https://timelinecovers.pro/facebook-cover/download/morning-road-facebook-cover.jpg', max_length=3000, null=True)),
                ('relationship', models.BooleanField()),
                ('followers', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('imageUrl', models.CharField(blank=True, max_length=800, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='group', to='socialmedia.group')),
                ('likes', models.ManyToManyField(to='socialmedia.Profile')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user2', to='socialmedia.profile')),
            ],
        ),
        migrations.AddField(
            model_name='group',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to='socialmedia.profile'),
        ),
        migrations.AddField(
            model_name='group',
            name='users',
            field=models.ManyToManyField(to='socialmedia.Profile'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post', to='socialmedia.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
