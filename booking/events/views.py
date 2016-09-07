from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.utils import timezone
from .models import Events


# Multipurpose group checks:
# Can be called as stardard function() or as
# @user_passes_test(fuction) !NOTE user_passes_test, passes user object so no need for parameters
def isTechnician(user):
    return user.groups.filter(name__in=['Technician']).exists()


def isBookingAssosiate(user):
    return user.groups.filter(name__in=['Booking Associate']).exists()


def isBookingManager(user):
    return user.groups.filter(name__in=['Booking Manager']).exists()


def isOrganizer(user):
    return user.groups.filter(name__in=['Organizer']).exists()


#   Standard views

@login_required(login_url='login/')
def home(request):
    # Checks if user is a technician
    if isTechnician(request.user):
        events = request.user.working_events.all().filter(
            ~Q(event_time__lt=timezone.datetime.now()) &
            Q(status__gt=2)
        )
        context = {
            'events': events
        }
        return render(request, 'dashboard-tech.html', context)
    #
    elif isBookingAssosiate(request.user):
        query_list = Events.objects.all().filter(~Q(event_time__lt=timezone.datetime.now()))
        drafts = query_list.filter(status=0)
        approved = query_list.filter(status=1)
        pending = query_list.filter(status=2)
        context = {
            'draft': drafts,
            'approved': approved,
            'pending': pending,
        }
        return render(request, 'dashboard-booking-associate.html', context)
    elif isBookingManager(request.user):
        # request content for booking manager here
        return render(request, 'dashboard-booking-manager.html', {})
    elif isOrganizer(request.user):
        # request content that is going to be used in organizer dahsboard here
        return render(request, 'dashboard-organizer.html', {})
    # sends superusers to admin view
    if request.user.is_superuser:
        return redirect('admin:index')
    # If somehow user is auth and not in any group
    raise PermissionDenied

