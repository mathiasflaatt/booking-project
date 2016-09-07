from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.utils import timezone
from .models import Events
from .form import EventForm


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


@login_required(login_url='login/')
def add(request):
    if not request.user.is_anonymous() and not isTechnician(request.user):
        form = EventForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.success(request, "Event was successfully added")
            return HttpResponseRedirect(instance.get_absolute_url())

        context = {
            "title": "Create new Event",
            'form': form
        }
        return render(request, 'events/form.html', context)
    else:
        raise Http404


def detail(request, slug=None):
    instance = get_object_or_404(Events, slug=slug)
    context = {
        'title': instance.title,
        'instance': instance,
        'workers': instance.workers
    }
    return render(request, 'events/detail.html', context)


def list(request):
    queryset_list = Events.objects.all().filter(event_time__gte=timezone.datetime.now())
    query = request.GET.get('q')
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query) |
            Q(band__name__icontains=query) |
            Q(location__name__icontains=query) |
            Q(band__genre__name__icontains=query)
        ).distinct()
    paginator = Paginator(queryset_list, 10)  # Show 10 contacts per page
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
        'title': 'Event overview',
        'queryset': queryset,
        'page_request_var': page_request_var
    }
    return render(request, 'events/list.html', context)
