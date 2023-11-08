from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *


def index(request):

    listings = AuctionListings.objects.filter(status=True)
    return render(request, "auctions/index.html", { 
        "listings": listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


# Create Listings
def create(request):
    if request.method =="POST":
        
        title = request.POST["title"]
        description = request.POST["description"]
        price = request.POST["price"]
        photo = request.POST["photo"]

        if not title or not price or not description or not photo:
            return render(request, "auctions/error.html", { 
                "message": "All inputs must be filled."
            })
        
        bid = Bids(user=request.user, bid=int(price))
        bid.save()

        category = Categories.objects.get(pk=int(request.POST["categories"]))
        AuctionListings.objects.create(title=title, description=description, price=price, bid=bid, photo=photo, created_by=request.user, category=category)

        return HttpResponseRedirect(reverse('index'))

    return render(request, "auctions/create.html", {
        "categories":Categories.objects.all()
    })
    
# Specific Listings
def listings(request, list_id):
    current_list = AuctionListings.objects.get(pk=int(list_id))
    in_watchlist = request.user in current_list.watchlists.all()

    if request.method == "POST":
        comment_text = request.POST.get("comment")

        if comment_text:
            comment = Comments.objects.create(comment_by=request.user, comment=comment_text, listing=current_list)
            comment.save()
        return HttpResponseRedirect(reverse("listings", args=(list_id, ))) 
    
    return render(request, "auctions/listings.html", { 
        "listings": current_list,
        "current_user": request.user,
        "in_watchlist": in_watchlist,
        "comments": Comments.objects.filter(listing=current_list)
    })


# Categories
def categories(request):
    listings = None
    
    if request.method == "POST":
        category = Categories.objects.get(pk=int(request.POST["categories"]))
        filtered_list = AuctionListings.objects.filter(category=category)

        return render(request, "auctions/categories.html", {
            "listing": category,
            "listings": filtered_list,
            "categories": Categories.objects.all()
        })
    
    return render(request, "auctions/categories.html", {
        "listings": listings,
        "categories": Categories.objects.all()
    })

# Watchlist
@login_required
def watchlists(request):
    user_watchlist = AuctionListings.objects.filter(watchlists=request.user)

    return render(request, "auctions/watchlists.html",{ 
        "listings": user_watchlist
    })

@login_required
def add_watchlist(request, list_id):
    current_list = AuctionListings.objects.get(pk=int(list_id))

    current_list.watchlists.add(request.user)
    return HttpResponseRedirect(reverse('listings', args=(list_id, )))

@login_required
def remove_watchlist(request, list_id):
    current_list = AuctionListings.objects.get(pk=int(list_id))

    current_list.watchlists.remove(request.user)
    return HttpResponseRedirect(reverse('listings', args=(list_id, )))

@login_required
def add_bid(request, list_id):
    new_bid = request.POST["bid"]
    current_list = AuctionListings.objects.get(pk=int(list_id))

    if new_bid and int(new_bid) > int(current_list.bid.bid):
        add_new_bid = Bids(user=request.user, bid=new_bid)
        add_new_bid.save()

        current_list.bid = add_new_bid
        current_list.save()
        return HttpResponseRedirect(reverse("listings", args=(list_id, )))
    else:
        return render (request, "auctions/error.html", { 
            "current_list": current_list,
            "message": "Your bid must be higher than the current bid."
        })
    
@login_required
def close_auction(request, list_id):
    current_list = AuctionListings.objects.get(pk=int(list_id))
    current_list.status = False
    
    current_list.save()
    return HttpResponseRedirect(reverse('listings', args=(list_id, )))