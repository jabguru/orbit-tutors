from django.db import models
from django.contrib.auth.models import User
from courses.utils import unique_slug_generator
from django.db.models.signals import pre_save, post_save


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    title = models.CharField(max_length=255, unique=True)
    author = models.ForeignKey(User, related_name='course', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=150, unique=True, null=True, blank=True)
    description = models.TextField()
    cost = models.IntegerField()
    featured_image = models.ImageField(upload_to='courses/%Y/%m/%d/', null=True, blank=False)
    attachment= models.FileField(upload_to='courses/attachments/%Y/%m/%d/', null=True, blank=True)
    published = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


def slug_save(sender, instance,*args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance, instance.title, instance.slug)


pre_save.connect(slug_save, sender=Course)
