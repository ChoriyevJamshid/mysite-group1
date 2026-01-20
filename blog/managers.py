from django.db.models import Manager
from blog.choices import PostStatus


class PublishedManager(Manager):

    def get_queryset(self):
        return super().get_queryset().filter(
            status=PostStatus.PUBLISHED
        )




