from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import now


class MyProfile(models.Model):
    objects = models.Manager()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(max_length=150, blank=True, null=True)
    image = models.ImageField(upload_to='profile_pics', null=True)


@receiver(post_save, sender=User)
def update_my_profile(sender, instance, created, **kwargs):
    if created:
        MyProfile.objects.create(user=instance)
        instance.myprofile.save()


class Post(models.Model):
    objects = models.Manager()
    DIARY_CHOICES = (
        ("public", "public"),
        ("private", "private"),
    )
    name = models.ForeignKey(User, on_delete=models.PROTECT, related_name='name')
    title = models.CharField(max_length=100, blank=False, null=False)
    slug = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=DIARY_CHOICES, default='public')
    content = models.TextField(max_length=1500, blank=False, null=False)
    date_posted = models.DateTimeField(default=timezone.now)
    liked = models.ManyToManyField(User, default=None, blank=True, related_name='liked')

    def __str__(self):
        return self.title

    def num_likes(self):
        return self.liked.all().count()

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk':self.pk})



class Like(models.Model):
    objects = models.Manager()
    LIKE_CHOICES = (
        ("Like", "Like"),
        ("Unlike", "Unlike"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, default='Like', max_length=10)

    def __str__(self):
        return str(self.post)


class PostComment(models.Model):
    objects = models.Manager()
    sno = models.AutoField(primary_key=True)
    comment = models.TextField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    reply = models.ForeignKey('PostComment', on_delete=models.CASCADE, null=True, related_name='replies')
    timestamp = models.DateTimeField(default=now)
