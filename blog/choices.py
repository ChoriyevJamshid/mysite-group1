from django.db.models import TextChoices


class PostStatus(TextChoices):
    DRAFT = "DR", "Draft"
    PUBLISHED = "PB", "Published"
