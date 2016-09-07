from django import template

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

@register.filter(name='status')
def status(number):
    STATUS_CHOICES = {
        0: 'Draft',
        1: 'Approved',
        2: 'Offer sent',
        3: 'Confirmed',
        4: 'Published'
    }
    return STATUS_CHOICES[number]