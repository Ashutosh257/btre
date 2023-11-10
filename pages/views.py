from django.shortcuts import render
from django.http import HttpResponse

from listings.models import Listing
from realtors.models import Realtor
from listings.choices import state_choices, price_choices, bedroom_choices

def index(req):
    listings = Listing.objects.order_by("-list_date").filter(is_published=True)[:3]

    context = {
        "listings" : listings,
        "state_choices": state_choices,
        "price_choices": price_choices,
        "bedroom_choices": bedroom_choices
    }

    return render(req, 'pages/index.html', context=context)

def about(req):

    realtors = Realtor.objects.all()[:3]

    mvp = Realtor.objects.filter(is_mvp=True)[0]

    context = {
        "realtors" : realtors,
        "mvp": mvp
    }
    return render(req, 'pages/about.html', context)