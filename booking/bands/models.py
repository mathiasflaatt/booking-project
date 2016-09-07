from django.db import models
from django.db.models.signals import pre_save
from django.core.urlresolvers import reverse
from django.utils.text import slugify


class Genre(models.Model):
    name = models.CharField(max_length=100)
    info = models.TextField()

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'


class Bands(models.Model):
    name = models.CharField(max_length=200)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    booking_fee = models.FloatField(null=False, default=0)
    bio = models.TextField()
    raider = models.TextField()
    contact = models.EmailField()
    slug = models.SlugField(unique=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('bands:detail', kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Band'
        verbose_name_plural = 'Bands'


def create_slug(instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    qs = Bands.objects.filter(slug=slug).order_by("id")
    exists = qs.exists()
    if exists:
        temp = slug.split("-")
        if temp[-1].isdigit():
            temp.remove(temp[-1])
            slug = "-".join(map(str, temp))
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug)
    else:
        return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver, sender=Bands)
