from django.contrib.auth.models import get_user_model
from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.urls import reverse
# Create your models here.

class Post(models.Model):

    STATUS_CHOICES = (
        ("draft", "draft"),
        ("published", "published")
    )

#DB Fields
    title = models.CharField(max_length= 250)
    slug = models.SlugField(max_length=300, unique=True, editable=False)
    author = models.ForeignKey(
        get_user_model(), blank=True, null=True, related_name="blog_posts", on_delete=models.CASCADE
    )
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    publish = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")

    class Meta:
        ordering = ("-publish",)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        pass

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={'slug': self.slug})