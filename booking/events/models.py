from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from bands.models import Bands


class Stages(models.Model):
    name = models.CharField(max_length=200, unique=True)
    capacity = models.IntegerField()
    lease = models.IntegerField()

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Stage'
        verbose_name_plural = 'Stages'


class Events(models.Model):
    DRAFT = 0
    APPROVED = 1
    SENT = 2
    SIGNED = 3
    PUBLISHED = 4
    STATUS_CHOICES = (
        (DRAFT, 'Draft'),
        (APPROVED, 'Approved'),
        (SENT, 'Offer sent'),
        (SIGNED, 'Confirmed'),
        (PUBLISHED, 'Published')
    )
    title = models.CharField(max_length=300)
    status = models.IntegerField(blank=False, choices=STATUS_CHOICES, default=0)
    location = models.ForeignKey(Stages)
    band = models.ForeignKey(Bands)
    event_time = models.DateTimeField(null=False, default=None)
    drafted = models.DateTimeField(auto_now_add=True, auto_now=False)
    last_changed = models.DateTimeField(auto_now_add=False, auto_now=True)
    member_tickets_price = models.IntegerField(null=False)
    normal_tickets_price = models.IntegerField(null=False)
    workers = models.ManyToManyField(User, related_name='working_events', help_text="Members helping with this event")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
