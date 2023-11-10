from django.shortcuts import render, get_object_or_404
from .models import Listing

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .choices import price_choices, bedroom_choices, state_choices

def index(req):
    listings = Listing.objects.order_by("-list_date").filter(is_published=True)

    paginator = Paginator(listings, per_page=3)
    page = req.GET.get("page")
    paged_listings = paginator.get_page(page)
    # paged_listings.adjusted_elided_pages = paginator.get_elided_page_range(page, on_each_side=2, on_ends=1)

    context = {
        "listings" : paged_listings
    }

    return render(req, template_name="listings/listings.html", context=context)

def listing(req, listing_id):
    
    listing = get_object_or_404(Listing, pk=listing_id)

    if req.user.is_authenticated:
        context = {
            'listing': listing,
            'user_data': req.user 
        }
    else:
        context = {
            'listing': listing
        }

    return render(req, template_name="listings/listing.html", context=context)


def search(req):
    
    # print(req.GET)

    filtered_query = Listing.objects.order_by("-list_date")

    for key, value in req.GET.items():
        if key == "keywords":
            filtered_query = filtered_query.filter(description__icontains=value)
        
        if req.GET[key] and key == "city":
            print("city")
            filtered_query = filtered_query.filter(city__iexact=value)
        
        if key == "state":
            filtered_query = filtered_query.filter(state__iexact=value)

        if key == "bedrooms":
            filtered_query = filtered_query.filter(bedrooms__lte=value)

        if key == "price":
            filtered_query = filtered_query.filter(price__lte=value)

    # print(filtered_query)

    context = {
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'listings': filtered_query,
        'values': req.GET
    }
    return render(req, template_name="listings/search.html", context=context)
