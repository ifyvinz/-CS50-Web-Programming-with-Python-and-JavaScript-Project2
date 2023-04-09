from email import message
from fileinput import close
from pickle import FALSE
from unicodedata import category
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Category, Auction, Bid, Comment, WatchList
from .forms import AuctionForm, BidForm,CloseForm,CommentForm


def index(request):
    list =   Auction.objects.filter(close=False).order_by("-listed_date")
    return render(request, "auctions/index.html", {
        "auctions": list
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

def newListing(request):
    
    if request.method == 'POST':
        form = AuctionForm(request.POST, request.FILES)
        if form.is_valid():
            
            title = form.cleaned_data["title"]
            discription = form.cleaned_data["discription"]
            category = form.cleaned_data["category"]
            currentPrice = form.cleaned_data["current_price"]
            startBid = form.cleaned_data["start_bid"]
            image = form.cleaned_data["image"]

            ol_category = Category.objects.filter(name=category).first()
            if not ol_category:
               cat = Category(name = category)
               cat.save()
           
               NewAuction = Auction(user = request.user, title = title, discription = discription, category = cat, current_price = currentPrice, start_bid = startBid, image = image)
               NewAuction.save()
               return HttpResponseRedirect(reverse("index"))
            NewAuction = Auction(user = request.user, title = title, discription = discription, category = ol_category, current_price = currentPrice, start_bid = startBid, image = image)
            NewAuction.save()
           
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request,"auctions/newListing.html",{
                'form': form
            } )
    return render(request, "auctions/newListing.html",{
             'form':AuctionForm()
    })

def listing(request, listing_id):
    #listing = Auction.objects.get(pk=listing_id)
    #if request.user is not listing.user:
    bid_message = ""
    winner = ""
    auction = Auction.objects.get(pk = listing_id)
    old_bid = Bid.objects.filter(listing = auction).first()
    comments = Comment.objects.filter(listing=auction)


    if old_bid:
        if old_bid.bidder == request.user and auction.close == True:
           winner = f"Congratulation {old_bid.bidder} You won the bid."
        elif old_bid.bidder == request.user:
            winner = f"{old_bid.bidder}, your ${old_bid.amount} bid is the current bid."
        elif old_bid.listing.user == request.user and auction.close == True:
            winner = f"{old_bid.bidder}, just won the auction with is the current bid of ${old_bid.amount}."
        else:
             winner = f"${old_bid.amount} bid is the current bid."

    if request.method == "POST":
        form = BidForm(request.POST, request.FILES)
        if form.is_valid():
          bid_amount = float(form.cleaned_data["amount"]) 
          if old_bid:
              if (bid_amount >= auction.start_bid and bid_amount > old_bid.amount):
                  old_bid.amount = bid_amount
                  old_bid.bidder = request.user
                  old_bid.save()
                  return HttpResponseRedirect(reverse("listing", kwargs={"listing_id":listing_id }))
              else:
                  bid_message = "Your Bid is Invalid. Place a bigger bid." 
          else:
              if bid_amount >= auction.start_bid:
                  new_bid = Bid(bidder = request.user, listing = auction, amount = bid_amount)
                  new_bid.save()
                  
                  return HttpResponseRedirect(reverse("listing", kwargs={"listing_id":listing_id }))
              else:
                   bid_message = "Your Bid is Invalid. Place a bigger bid." 
    
    return render(request, "auctions/listing.html",{
        "listing": auction,
        "form": BidForm(),
        "error_message": bid_message,
        "winner_message": winner,
        "comments": comments
    })

def betweenWatchList(request, listing_id):
    if request.method == "POST":
        auction = Auction.objects.get(pk=listing_id)
        print(auction.id)
        print(auction.title)
        #watch = WatchList(user=request.user)
        #watch.save()
        watch = WatchList.objects.filter(listing = auction, user = request.user)
        #print(watch)
        if watch:
             #print(watch.user)
            print("Deleted")
            watch.delete()
            
            return HttpResponseRedirect(reverse("listing", kwargs={"listing_id":listing_id }))
        
        watch = WatchList(user = request.user)
        watch.save()
        watch.listing.add(auction)
        print(watch)
        print("Added")
        return HttpResponseRedirect(reverse("listing", kwargs={"listing_id":listing_id }))
        
           
    print("I am here")
    return HttpResponseRedirect(reverse("index"))

def bidding(request, listing_id):
    auction = Auction.objects.get(pk = listing_id)
    old_bid = Bid.objects.filter(listing = auction)
    auction.bid_count= 5
    auction.save()
    if request.method == "POST":
        form = BidForm(request.POST, request.FILES)
        if form.is_valid():
          bid_amount = form.cleaned_data["amount"] 
          if old_bid:
              if bid_amount >= auction.start_bid and bid_amount > old_bid.amount:
                  old_bid.amount = bid_amount
                 
              else:
                  error_message = "Your Bid is Invalid. Place a bigger bid."
          else:
              if bid_amount >= auction.start_bid:
                  new_bid = Bid(bidder = request.user, listing = auction, amount = bid_amount)
                  new_bid.save()
                  auction.bid_count= 5
                  auction.save()
              else:
                   error_message = "Your Bid is Invalid. Place a bigger bid."
    
    
    
    elif request.method == "GET":
        return render(request, "auctions/bid.html",{
             'form':BidForm()
       })

def close(request, listing_id):
    auction = Auction.objects.get(pk = listing_id)

    if not request.method == "POST":
        return render(request, "auctions/listing.html",  {
           "listing": auction,
          
        } )

    close = request.POST["close"]
    auction.close = close
    auction.save()
    return HttpResponseRedirect(reverse("listing", kwargs={"listing_id":listing_id }))

@login_required(login_url='/login')
def add_comment(request, listing_id):
    listing = Auction.objects.get(pk=listing_id)

    if not request.method == "POST":
        return render(request, "auctions/comment.html", {
            "form": CommentForm(),
            "listing": listing
        })

    form = CommentForm(request.POST or None)

    if not form.is_valid():
        return render(request, "auctions/comment.html", {
            "form": form
        })
    
    title = form.cleaned_data["title"]
    message = form.cleaned_data["message"]
    form = Comment(user = request.user, listing = listing, title = title, message = message)
    #form.user = request.user
    form.save()
    
    return HttpResponseRedirect(reverse("listing", kwargs={"listing_id":listing_id }))

@login_required(login_url='/login')
def watchLister(request):
    watch = WatchList.objects.filter(user = request.user)
    return render(request, "auctions/watchList.html", {
        "watchList":watch
    })
@login_required(login_url='/login')
def categories(request):
    #categories = Category.objects.all()
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

@login_required(login_url='/login')
def listingCategory(request, listing_cat):
    
    listings = Auction.objects.filter(category=listing_cat)
    return render(request, "auctions/listingCategory.html", {
        "listings": listings
    })

    


    

