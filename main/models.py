from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            unique_slug = base_slug
            counter = 1
            while True:
                if Post.objects.filter(slug=unique_slug).exclude(pk=self.pk).exists():
                    unique_slug = f"{base_slug}-{counter}"
                    counter += 1
                else:
                    break
            self.slug = unique_slug
        super(Post, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.title} :- {self.description}"
    



