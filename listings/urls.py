
from django.urls import path
from . import views

urlpatterns = [
    path("", view=views.index, name='listings'),
    path("<int:listing_id>", view=views.listing, name='listing'),
    path("search", view=views.search, name='search'),
]