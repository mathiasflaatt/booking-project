from django.contrib import admin
from .models import Events, Stages

class EventAdmin(admin.ModelAdmin):
    list_display = [u'title', u'event_time', u'last_changed', u'status']
    list_filter = ['event_time', 'last_changed', u'status', u'location']
    search_fields = ['title', 'band']

    class Meta:
        model = Events

admin.site.register(Events, EventAdmin)
admin.site.register(Stages)
# Register your models here.
