from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name = 'profile_user')
    friends = models.ManyToManyField(User, related_name= 'friends')
    first_name = models.CharField(max_length= 100)
    last_name = models.CharField(max_length= 100)
    city = models.CharField(max_length= 200)
    dob = models.DateField()
    imageUrl = models.CharField(max_length= 3000, blank= True, null= True, default='https://www.adobe.com/express/create/media_127540366421d3d5bfcaf8202527ca7d37741fd5d.jpeg?width=400&format=jpeg&optimize=medium')
    coverUrl = models.CharField(max_length= 3000, blank= True, null= True, default='https://timelinecovers.pro/facebook-cover/download/morning-road-facebook-cover.jpg')
    relationship = models.BooleanField()

    def __str__(self):
        return self.first_name


class Group(models.Model):
    name = models.CharField(max_length= 50)
    description = models.CharField(max_length= 1000)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name= 'owner')
    users = models.ManyToManyField(Profile)

    def __str__(self):
        return self.name



class Post(models.Model):
    user = models.ForeignKey(Profile, on_delete= models.CASCADE, related_name= 'user2')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True, related_name= 'group')
    body = models.TextField()
    imageUrl = models.CharField(max_length=800, blank=True, null=True)
    likes = models.ManyToManyField(Profile)
    created = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return self.body


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    post = models.ForeignKey(Post, on_delete= models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return self.body