from django.contrib.postgres.fields import JSONField
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.dispatch import receiver


from ..users.models import User


class Wishlist(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=2500)
    date_created = models.DateField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(User)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_of_wishlist', default='')
    is_public = models.BooleanField(default=True)
    slug = models.SlugField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Generating simply slug during creation
        """
        if not self.slug:
            self.slug = '{0}-{1}'.format(slugify(self.name), self.pk)

        return super(Wishlist, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'wishlist-detail',
            kwargs={'slug': self.slug,}
        )


class Item(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=350)
    date_created = models.DateField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True)
    raw_data = JSONField(blank=True, null=True)
    user_input = JSONField(blank=True, null=True, default='{}')
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)

    def update_price(self):
        pass

    def get_absolute_url(self):
        return reverse('item:detail',
                       kwargs={'pk': self.pk})

    def __str__(self):
        return self.name


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
