from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

from blog.choices import PostStatus
from utils import BaseModel


class Post(BaseModel):

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    author = models.ForeignKey(get_user_model(),
                               on_delete=models.CASCADE,
                               related_name='posts')

    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=15,
                              choices=PostStatus.choices,
                              default=PostStatus.DRAFT)

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]

    def __str__(self):
        return self.title
