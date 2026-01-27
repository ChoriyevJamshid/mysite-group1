from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import slugify


from blog.choices import PostStatus
from blog.managers import PublishedManager
from utils import BaseModel


class Post(BaseModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,
                            unique_for_date='publish')
    author = models.ForeignKey(get_user_model(),
                               on_delete=models.CASCADE,
                               related_name='posts')

    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=15,
                              choices=PostStatus.choices,
                              default=PostStatus.DRAFT)

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       kwargs={"year": self.publish.year,
                               "month": self.publish.month,
                               "day": self.publish.day,
                               "slug": self.slug})


class Comment(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=63)
    email = models.EmailField()
    body = models.TextField()

    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['created_at'])
        ]

    def __str__(self):
        return self.name


