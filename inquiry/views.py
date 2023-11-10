from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Inquiry

def inquiry(req):

    if req.method == "POST":

        user_id = req.POST["user_id"]
        realtor_name = req.POST["realtor_name"]
        realtor_email = req.POST["realtor_email"]
        listing_id = req.POST["listing_id"]
        listing_name = req.POST["listing"]
        name = req.POST["name"]
        email = req.POST["email"]
        phone = req.POST["phone"]
        message = req.POST["message"]

        listings_inquired = Inquiry.objects.filter(listing_id=listing_id)

        if req.user.is_authenticated and listings_inquired.filter(user_id=user_id).exists():
            messages.error(req, message=f"Your have already submitted an inquiry for listing: {listing_name} , a realtor will get back to you soon!")
            return redirect('/listings/' + listing_id)
        elif not req.user.is_authenticated and listings_inquired.filter(email=email).exists():
            messages.error(req, message=f"Your have already submitted an inquiry for listing: {listing_name} , a realtor will get back to you soon!")
            return redirect('/listings/' + listing_id)
        else:
            inquiry = Inquiry.objects.create(
                listing=listing_name,
                listing_id=listing_id,
                name=name,
                email=email,
                phone=phone,
                message=message,
                user_id=user_id,
                )

            inquiry.save()

            messages.success(req, message=f"Your inquiry has been sent successfully for listing: {listing_name} , a realtor will get back to you soon at {email}!")
            return redirect('/listings/' + listing_id)
    else:
        messages.error(req, message="Inquiry has been failed!")
        return redirect('index')
