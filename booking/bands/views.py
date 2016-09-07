from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Bands
from .form import BandForm


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


# Standard views

def home(request):
    queryset_list = Bands.objects.all()
    query = request.GET.get('q')
    if query:
        queryset_list = queryset_list.filter(
            Q(name__icontains=query) |
            Q(bio__icontains=query) |
            Q(genre__name__icontains=query)
        ).distinct()
    paginator = Paginator(queryset_list, 10)  # Show 25 contacts per page
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
        'title': 'Band overview',
        'queryset': queryset,
        'page_request_var': page_request_var
    }
    return render(request, 'bands/list.html', context)


@login_required(login_url='login/')
def add(request):
    if not request.user.is_anonymous() and not isTechnician(request.user):
        form = BandForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.success(request, "Band was successfully added")
            return HttpResponseRedirect(instance.get_absolute_url())

        context = {
            "title": "Create",
            'form': form
        }
        return render(request, 'bands/form.html', context)
    else:
        raise Http404


def detail(request, slug=None):
    instance = get_object_or_404(Bands, slug=slug)
    events = instance.events_set.all().filter(
        Q(status__gt=3) &
        Q(event_time__gte=timezone.datetime.now())
        )
    context = {
        'title': instance.name,
        'instance': instance,
        'events': events
    }
    return render(request, 'bands/detail.html', context)
