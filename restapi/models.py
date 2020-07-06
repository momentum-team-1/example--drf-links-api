from django.db import models
from users.models import User
from taggit.managers import TaggableManager
from ordered_model.models import OrderedModel


class Link(models.Model):
    owner = models.ForeignKey(to=User,
                              related_name="links",
                              on_delete=models.CASCADE)
    url = models.URLField()
    title = models.CharField(max_length=255)
    tags = TaggableManager()

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['owner', 'url'],
                                    name="unique_url_by_owner")
        ]


class PageLink(OrderedModel):
    link = models.ForeignKey(to=Link,
                             on_delete=models.CASCADE,
                             related_name='+')
    page = models.ForeignKey(to='Page',
                             on_delete=models.CASCADE,
                             related_name='+')
    order_with_respect_to = 'page'

    class Meta(OrderedModel.Meta):
        pass


class Page(models.Model):
    owner = models.ForeignKey(to=User,
                              related_name="pages",
                              on_delete=models.CASCADE)
    topic = models.CharField(max_length=255)
    slug = models.SlugField()
    links = models.ManyToManyField(to=Link, through=PageLink)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['owner', 'slug'],
                                    name="unique_slug_by_owner")
        ]
